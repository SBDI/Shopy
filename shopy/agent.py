# agent.py
from typing import List, Dict, Optional, Any
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
import asyncio
import logging
import os
from tavily import TavilyClient

# Relative imports based on your project structure
from .llm import GeminiLLM, MockLLM
from .models import State
from .prompts import email_template_prompt
from .configs.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Tavily client
config = Config()
tavily_client = TavilyClient(api_key=config.tavily_api_key) if config.tavily_api_key else None

if config.google_api_key:
    os.environ['GOOGLE_API_KEY'] = config.google_api_key  # set as environment variable
    llm = GeminiLLM()
elif config.gmail_user and config.gmail_pass and config.youtube_api_key and config.tavily_api_key:
    llm = MockLLM()  # Fall back to MockLLM if Groq API key is not available
else:
    llm = MockLLM()
    logging.warning("No valid API keys provided, using MockLLM.")


# Define node functions directly in agent.py
async def tavily_search_node(state: State) -> State:
    """Perform a search using the Tavily API."""
    if not tavily_client:
        logging.warning("Tavily API key not configured. Using mock search results.")
        state.products = [
            {"name": "Product A", "price": 100},
            {"name": "Product B", "price": 150},
        ]
        return state
    try:
        search_results = tavily_client.search(query=state.query, search_depth="3")
        if search_results and isinstance(search_results, dict) and search_results.get("results"):
            state.products = [{"name": item.get("title"), "url": item.get("url")} for item in search_results["results"]]
            logging.info(f"Tavily search completed successfully for query: {state.query}")
        else:
            logging.warning(f"Tavily search returned no results for query: {state.query}")
            state.products = []

    except Exception as e:
        logging.error(f"Error during Tavily search: {e}")
        state.products = []

    return state

async def schema_mapping_node(state: State) -> State:
    """Map the search results to a schema."""
    # Mock implementation
    state.product_schema = [
        {"name": "Product A", "specs": {"processor": "Snapdragon 888", "battery": "4500mAh"}},
        {"name": "Product B", "specs": {"processor": "A15 Bionic", "battery": "5000mAh"}},
    ]
    return state

async def product_comparison_node(state: State) -> State:
    """Compare products based on their specs and reviews."""
    # Mock implementation
    state.comparison = [
        {"product_name": "Product A", "rating": 4.5},
        {"product_name": "Product B", "rating": 4.7},
    ]
    state.best_product = {"product_name": "Product B", "justification": "Better rating and specs"}
    return state

async def youtube_review_node(state: State) -> State:
    """Fetch a YouTube review link for the best product."""
    # Mock implementation
    if state.best_product and state.best_product["product_name"]:
        product_name = state.best_product["product_name"]
        state.youtube_link = f"https://www.youtube.com/watch?v=mock-review-{product_name.replace(' ', '-')}"
        logging.info(f"Mock YouTube link generated for {product_name}")
    else:
         state.youtube_link = ""
         logging.warning("No best product to generate a youtube link")
    return state

async def generate_summary_node(state: State) -> State:
    """Generate a summary of the products using the LLM."""
    if not state.products:
        logging.warning("No products to summarize.")
        return state
    
    try:
        product_names = [product.get("name") for product in state.products if product.get("name")]
        if not product_names:
            logging.warning("No valid product names to summarize.")
            return state

        prompt = f"Summarize the following products: {', '.join(product_names)}"
        messages = [{"role": "user", "content": prompt}]
        logging.debug(f"Messages type: {type(messages)}, value: {messages}") # Debugging
        summary = await llm.agenerate(messages=messages)
        state.summary = summary
        logging.info(f"Summary generated: {summary}")
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
    return state


async def display_node(state: State) -> State:
    """Display the results to the user."""
    state.display_data = {
        "products": state.products,
        "best_product": state.best_product,
        "comparison": state.comparison,
        "youtube_link": state.youtube_link,
         "summary": state.summary,
    }
    return state

async def send_email_node(state: State) -> State:
    """Send an email recommendation to the user."""
    # Mock implementation
    email = state.email
    product_name = state.best_product["product_name"]
    justification = state.best_product["justification"]
    logging.info(f"Sending email to {email} about {product_name}: {justification}")
    return state

class ShopyAgent:
    """A class to orchestrate multiple tools using LangGraph."""

    def __init__(self):
        """Initialize ShopyAgent with necessary components."""
        self.workflow = self.create_graph()

    def create_graph(self) -> StateGraph:
        """Create a LangGraph state graph workflow."""
        builder = StateGraph(State)
        builder.add_node("tavily_search", tavily_search_node)
        builder.add_node("schema_mapping", schema_mapping_node)
        builder.add_node("product_comparison", product_comparison_node)
        builder.add_node("youtube_review", youtube_review_node)
        builder.add_node("generate_summary", generate_summary_node) # Added summary node
        builder.add_node("display", display_node)
        builder.add_node("send_email", send_email_node)
        builder.add_edge(START, "tavily_search")
        builder.add_edge("tavily_search", "schema_mapping")
        builder.add_edge("schema_mapping", "product_comparison")
        builder.add_edge("product_comparison", "youtube_review")
        builder.add_edge("youtube_review", "generate_summary") # Added edge to summary node
        builder.add_edge("generate_summary", "send_email")
        builder.add_edge("send_email", "display")
        builder.add_edge("display", END)


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
            summary = "",  # Initialize the summary field
        )
        final_state = await self.workflow.ainvoke(state)
        return final_state