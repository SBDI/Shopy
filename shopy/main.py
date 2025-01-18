# main.py

import asyncio
import os
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import logging

# Relative imports based on your project structure
from .llm import GeminiLLM, MockLLM
from .models import State
from .configs.config import Config
from .agent import ShopyAgent
from .utils.rich_utils import clean_llm_output # Modified import
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def load_json_and_test(query, email):
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
        final_state = await agent.run(query, email)  # Run the workflow
        console = Console()

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

                    md = Markdown(f"Comparisons: {str(display_data['comparison'])}")
                    panel = Panel(md, title="Comparison:", border_style="blue")
                    console.print(panel)

                return final_state.dict()
        return {}
    except Exception as e:
        logging.error(f"Main function error: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None

if __name__ == "__main__":
    query = input("Enter your product query: ")
    email = input("Enter your email: ")
    asyncio.run(load_json_and_test(query, email))