# shopy/tools.py
from typing import List, Dict, Any, Optional
import logging
import asyncio
import google.generativeai as genai
from tavily import TavilyClient
from email.message import EmailMessage
import ssl
import smtplib

from shopy.exceptions import (
    TavilySearchError,
    DataStructuringError,
    ProductComparisonError,
    YouTubeReviewError,
    LLMError,
    EmailError,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TavilyTool:
    """A tool for searching using the Tavily API."""

    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key) if api_key else None

    async def search(self, query: str) -> List[Dict[str, str]]:
        """Searches for products using the Tavily API."""
        if not self.client:
            logging.warning("Tavily API key not configured. Using mock search results.")
            return [
                {"name": "Product A", "price": 100},
                {"name": "Product B", "price": 150},
            ]
        try:
            search_results = self.client.search(query=query, search_depth="3")
            if search_results and isinstance(search_results, dict) and search_results.get("results"):
                products = [{"name": item.get("title"), "url": item.get("url")} for item in search_results["results"]]
                logging.info(f"Tavily search completed successfully for query: {query}")
                return products
            else:
                logging.warning(f"Tavily search returned no results for query: {query}")
                return []
        except Exception as e:
            logging.error(f"Error during Tavily search: {e}")
            raise TavilySearchError(f"Error during Tavily search: {e}")


class DataStructuringTool:
    """A tool for structuring product data."""

    async def map_schema(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Maps the product data to a defined schema."""
        # Mock implementation
        logging.info("Structuring product data using mock implementation.")
        try:
            structured_products = [
                {"name": "Product A", "specs": {"processor": "Snapdragon 888", "battery": "4500mAh"}},
                {"name": "Product B", "specs": {"processor": "A15 Bionic", "battery": "5000mAh"}},
            ]
            return structured_products
        except Exception as e:
            logging.error(f"Error during data structuring: {e}")
            raise DataStructuringError(f"Error during data structuring: {e}")


class YouTubeTool:
    """A tool for fetching YouTube review links."""

    async def fetch_review_link(self, best_product: Optional[Dict[str, Any]]) -> str:
        """Fetches a YouTube review link for a given product."""
        # Mock implementation
        try:
            if best_product and best_product.get("product_name"):
                product_name = best_product["product_name"]
                mock_link = f"https://www.youtube.com/watch?v=mock-review-{product_name.replace(' ', '-')}"
                logging.info(f"Mock YouTube link generated for {product_name}")
                return mock_link
            else:
                logging.warning("No best product to generate a YouTube link.")
                return ""
        except Exception as e:
            logging.error(f"Error during youtube review: {e}")
            raise YouTubeReviewError(f"Error during youtube review: {e}")


class ProductComparisonTool:
    """A tool for comparing products."""

    async def compare_products(self, state) -> Dict[str, Any]:
        """Compares products based on their specs and reviews."""
        # Mock implementation
        logging.info("Comparing products using mock implementation.")
        try:
            comparison = [
                {"product_name": "Product A", "rating": 4.5},
                {"product_name": "Product B", "rating": 4.7},
            ]
            best_product = {"product_name": "Product B", "justification": "Better rating and specs"}
            return {"comparison": comparison, "best_product": best_product}
        except Exception as e:
            logging.error(f"Error during product comparison: {e}")
            raise ProductComparisonError(f"Error during product comparison: {e}")


class EmailTool:
    """A tool to send emails using Gmail."""

    def __init__(self, gmail_user, gmail_pass):
        self.gmail_user = gmail_user
        self.gmail_pass = gmail_pass
        self.port = 465
        self.smtp_server = "smtp.gmail.com"


    async def send_email(self, state, email_template_prompt, llm):
       try:
          if not self.gmail_user or not self.gmail_pass:
              logging.warning("Gmail user or password not configured. Email will not be sent.")
              return
          # Generate email content using the LLM
          prompt = email_template_prompt.format(
             product_name=state.best_product["product_name"],
             justification_line=state.best_product["justification"],
             user_query=state.query,
          )
          messages = [{"role": "user", "content": prompt}]
          email_content = await llm.agenerate(messages=messages)
          if not email_content:
            logging.warning("No email content generated, email will not be sent")
            return

          logging.debug(f"Email content: {email_content}")
          #Parse the email content

          # Create email message
          email_msg = EmailMessage()
          email_msg["From"] = self.gmail_user
          email_msg["To"] = state.email
          # Parse the JSON string
          import json
          parsed_email_content = json.loads(email_content)
          email_msg["Subject"] = parsed_email_content.get("subject", "Product Recommendation")
          email_msg.set_content(f"""
             {parsed_email_content.get("heading", "Recommendation for you")}
             {parsed_email_content.get("justification_line", "We have the best product for you")}
          """)


          # Send email
          context = ssl.create_default_context()
          with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
              server.login(self.gmail_user, self.gmail_pass)
              server.send_message(email_msg)
              logging.info(f"Email sent successfully to {state.email}")

       except Exception as e:
           logging.error(f"Error during email sending: {e}")
           raise EmailError(f"Error during email sending {e}")