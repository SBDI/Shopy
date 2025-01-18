# main.py
import asyncio
import os
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
import logging

# Absolute imports
from shopy.llm import GeminiLLM, MockLLM
from shopy.models import State
from shopy.config import Config
from shopy.agent import ShopyAgent
from shopy.utils import clean_llm_output

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

console = Console(theme=custom_theme)


async def main(query:str = None, email:str = None):
    """Run the ShopyAgent workflow with the given query and email."""
    logging.info("ShopyAgent is starting...")

    try:
        config = Config()
        if config.google_api_key:
            llm = GeminiLLM()
        elif config.gmail_user and config.gmail_pass and config.youtube_api_key and config.tavily_api_key:
            llm = MockLLM()  # Fall back to MockLLM if Groq API key is not available
        else:
            llm = MockLLM()
            logging.warning("No valid API keys provided, using MockLLM.")

        if not await llm.check_auth():
             logging.error("LLM authentication failed. Please check your API key.")
             return None

        agent = ShopyAgent()  # Initialize the ShopyAgent
        
        if not query:
            query = input("Enter your product query: ")
        if not email:
             email = input("Enter your email: ")
        final_state = await agent.run(query, email)  # Run the workflow
        

        if isinstance(final_state, State):
            display_data = final_state.display_data
            if display_data:
                if display_data["products"] and display_data["best_product"]:
                    console.print(f"\n[bold]Here is what ShopyAgent suggests: [/bold] {display_data['best_product']['product_name']}")

                    md = Markdown(f"Justification:\n {display_data['best_product']['justification']}")
                    panel = Panel(md, title="Best Product", border_style="blue")
                    console.print(panel)

                    md = Markdown(f"See the review here: {display_data['youtube_link']}")
                    panel = Panel(md, title="YouTube Review Link", border_style="blue")
                    console.print(panel)

                    # Create a table for product comparison
                    table = Table(title="Product Comparisons",show_lines=True)
                    table.add_column("Product Name", style="cyan")
                    table.add_column("Rating", style="magenta")

                    for item in display_data['comparison']:
                        table.add_row(item.get('product_name', ''), str(item.get('rating', '')))
                    console.print(table)

                    console.print(f"\n[info]Summary:[/info]")
                    clean_llm_output(display_data['summary'], console)

                return final_state.dict()
        return {}
    except Exception as e:
        logging.error(f"Main function error: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None