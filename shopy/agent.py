# shopy/agent.py
from typing import List, Dict, Optional, Any
from langgraph.graph import StateGraph, START, END
import asyncio
import logging
import os

# Absolute imports
from shopy.llm import GeminiLLM, MockLLM
from shopy.models import State
from shopy.prompts import email_template_prompt
from shopy.config import Config
from shopy.tools import (
    TavilyTool,
    DataStructuringTool,
    YouTubeTool,
    ProductComparisonTool,
    EmailTool,
     DisplayTool,
)
from shopy.exceptions import (
    TavilySearchError,
    DataStructuringError,
    ProductComparisonError,
    YouTubeReviewError,
    LLMError,
    EmailError,
)
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Define a custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "header": "bold magenta",
    "best_product": "bold green",
})


# Initialize configuration
config = Config()

# Initialize LLM
if config.google_api_key:
    os.environ['GOOGLE_API_KEY'] = config.google_api_key
    llm = GeminiLLM()
elif config.gmail_user and config.gmail_pass and config.youtube_api_key and config.tavily_api_key:
    llm = MockLLM()
else:
    llm = MockLLM()
    logging.warning("No valid API keys provided, using MockLLM.")

# Initialize Tools
tavily_tool = TavilyTool(api_key=config.tavily_api_key)
data_structuring_tool = DataStructuringTool()
youtube_tool = YouTubeTool()
product_comparison_tool = ProductComparisonTool()
email_tool = EmailTool(gmail_user=config.gmail_user, gmail_pass=config.gmail_pass)
display_tool = DisplayTool()

# Node functions
async def tavily_search_node(state: State) -> State:
    """Perform a search using the Tavily API."""
    try:
        state.products = await tavily_tool.search(state.query)
        logging.debug(f"Tavily search products: {state.products}, query: {state.query}")
        return state
    except TavilySearchError as e:
        logging.error(f"Tavily search error: {e}, query: {state.query}")
        state.products = []
        return state
    except Exception as e:
        logging.error(f"Unexpected error in tavily_search_node: {e}, query: {state.query}")
        state.products = []
        return state


async def schema_mapping_node(state: State) -> State:
    """Map the search results to a schema."""
    try:
        state.product_schema = await data_structuring_tool.map_schema(state.products)
        logging.debug(f"product_schema: {state.product_schema}, products:{state.products}")
        return state
    except DataStructuringError as e:
        logging.error(f"Data structuring error: {e}, products:{state.products}")
        state.product_schema = []
        return state
    except Exception as e:
        logging.error(f"Unexpected error in schema_mapping_node: {e}, products:{state.products}")
        state.product_schema = []
        return state


async def product_comparison_node(state: State) -> State:
    """Compare products based on their specs and reviews."""
    try:
        logging.debug(f"product_comparison_node - Input: product_schema: {state.product_schema}, products: {state.products}")
        comparison_data = await product_comparison_tool.compare_products(state)
        state.comparison = comparison_data.get("comparison", [])
        state.best_product = comparison_data.get("best_product", {})
        logging.debug(f"product_comparison_node - Output: comparison: {state.comparison}, best_product: {state.best_product}")
        return state
    except ProductComparisonError as e:
        logging.error(f"Product comparison error: {e}, products: {state.products}, product_schema:{state.product_schema}")
        state.comparison = []
        state.best_product = {}
        return state
    except Exception as e:
        logging.error(f"Unexpected error in product_comparison_node: {e}, products: {state.products}, product_schema:{state.product_schema}")
        state.comparison = []
        state.best_product = {}
        return state


async def youtube_review_node(state: State) -> State:
    """Fetch a YouTube review link for the best product."""
    try:
       logging.debug(f"youtube_review_node - Input: best_product: {state.best_product}")
       state.youtube_link = await youtube_tool.fetch_review_link(state.best_product)
       logging.debug(f"youtube_review_node - Output: youtube_link: {state.youtube_link}")
       return state
    except YouTubeReviewError as e:
        logging.error(f"YouTube review error: {e}, best_product: {state.best_product}")
        state.youtube_link = ""
        return state
    except Exception as e:
        logging.error(f"Unexpected error in youtube_review_node: {e}, best_product: {state.best_product}")
        state.youtube_link = ""
        return state


async def generate_summary_node(state: State) -> State:
    """Generate a summary of the products using the LLM."""
    if not state.products:
        logging.warning("No products to summarize.")
        return state
    
    try:
        product_names = [product.get("name") for product in state.products if product.get("name")]
        if not product_names:
            logging.warning(f"No valid product names to summarize.: {state.products}")
            return state

        prompt = f"""
          You are a product expert.
          Your goal is to analyze a list of products and generate a concise summary that contains a single paragraph with the key features and unique benefits for each product.
          The products to analyze are: {', '.join(product_names)}.
          Provide the output in the following format:
          ```
          * **Product Name 1**: Explanation
          * **Product Name 2**: Explanation
          ```
          """
        messages = [{"role": "user", "content": prompt}]
        logging.debug(f"generate_summary_node - LLM Input: products: {state.products}, prompt: {prompt}")
        summary = await llm.agenerate(messages=messages)
        state.summary = summary
        logging.info(f"Summary generated: {summary}")
        return state
    except LLMError as e:
        logging.error(f"LLM error: {e}, products: {state.products}")
        state.summary = ""
        return state
    except Exception as e:
        logging.error(f"Unexpected error in generate_summary_node: {e}, products: {state.products}")
        state.summary = ""
        return state


async def display_node(state: State) -> State:
    """Display the results to the user."""
    await display_tool.display_data(state.display_data)
    return state

async def send_email_node(state: State) -> State:
    """Send an email recommendation to the user."""
    try:
        logging.debug(f"send_email_node - email inputs: email: {state.email}, product: {state.best_product}")
        await email_tool.send_email(state=state, email_template_prompt=email_template_prompt, llm=llm)
        return state
    except EmailError as e:
        logging.error(f"Email error: {e}, email: {state.email}, product: {state.best_product}")
        return state
    except Exception as e:
        logging.error(f"Unexpected error in send_email_node: {e}, email: {state.email}, product: {state.best_product}")
        return state

class ShopyAgent:
    """A class to orchestrate multiple tools using LangGraph."""

    def __init__(self):
        """Initialize ShopyAgent with necessary components."""
        self.workflow = self.create_graph()
        self.console = Console(theme=custom_theme) # Added console as an instance variable

    def create_graph(self) -> StateGraph:
        """Create a LangGraph state graph workflow."""
        builder = StateGraph(State)
        builder.add_node("tavily_search", tavily_search_node)
        builder.add_node("schema_mapping", schema_mapping_node)
        builder.add_node("product_comparison", product_comparison_node)
        builder.add_node("youtube_review", youtube_review_node)
        builder.add_node("generate_summary", generate_summary_node)
        builder.add_node("display", display_node)
        builder.add_node("send_email", send_email_node)
        builder.add_edge(START, "tavily_search")
        builder.add_edge("tavily_search", "schema_mapping")
        builder.add_edge("schema_mapping", "product_comparison")
        builder.add_edge("product_comparison", "youtube_review")
        builder.add_edge("youtube_review", "generate_summary")
        builder.add_edge("generate_summary", "display") # Reverted to the correct order
        builder.add_edge("display", "send_email")  # Reverted to the correct order
        builder.add_edge("send_email", END)

        return builder.compile()

    async def run(self, query: str, email: str) -> State:
        """Execute the ShopyAgent workflow with the given query and email."""
        state = State(
            query=query,
            email=email,
            products=[],
            product_schema=[],
            blogs_content=[],
            best_product={},
            comparison=[],
            youtube_link="",
            display_data={},
            summary = "",
        )
        final_state = await self.workflow.ainvoke(state)
        return final_state