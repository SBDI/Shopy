# llm.py

from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from .exceptions import LLMError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiLLM:
    """
    A class to interact with Google's Gemini model through their API.
    This implementation uses google-generativeai client for asynchronous operations.
    """

    def __init__(self):
        """Initialize GeminiLLM with API key from config."""
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self._is_authenticated = False

    async def check_auth(self) -> bool:
        """Verify API authentication with a test request."""
        try:
            response = await self.agenerate([{"role": "user", "content": "test"}])
            if response:
                self._is_authenticated = True
                logging.info("Gemini API authentication successful.")
                return True
            else:
                logging.error("Gemini API authentication failed.")
                return False
        except Exception as e:
            logging.error(f"❌ Authentication failed: {str(e)}")
            return False

    async def agenerate(self, messages: List[Dict], temperature: Optional[float] = None) -> str:
        """Generate text using the Gemini API."""
        try:
            # Ensure messages are a list of dictionaries with 'role' and 'content' keys
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                    formatted_messages.append(msg)
                else:
                    logging.warning(f"Invalid message format: {msg}. Skipping.")
            if not formatted_messages:
                 logging.error("No valid messages provided to Gemini API.")
                 return ""
            prompt = ""
            for msg in formatted_messages:
                prompt += f"{msg['content']}\n"

            response = await self.model.generate_content_async(
              prompt,
              generation_config=genai.types.GenerationConfig(
                  temperature=temperature if temperature else 0.5,
                  max_output_tokens=1024
              )
            )
            return response.text
        except Exception as e:
            logging.error(f"Error generating text with Gemini API: {e}")
            raise LLMError(f"Error generating text with Gemini API: {e}")

class MockLLM:
    """A mock LLM class for testing purposes."""

    def __init__(self):
        self._is_authenticated = True
        self.responses = {
            "plan": "Thought: Analyzing student information and planning a comprehensive approach. Action: Combining calendar, task, and profile insights for an optimal study schedule. Observation: Prioritizing tasks, accommodating all engagements. Decision: A balanced schedule combining high-focus work with necessary breaks and personal time.",
            "materials": "Thought: Identifying the appropriate visual, concise elements for content summarization. Action: Extracting key information and formatting in a mind-map and color-coded style. Observation: Emphasizing time-saving methods and the ADHD profile characteristics. Decision: A formatted response with essential information tailored to the student's preferences.",
            "strategies": "Thought: Considering the student's schedule and needs to provide effective advice. Action: Combining information from different sources to create a balanced plan. Observation: Focusing on focus areas and practical steps for daily planning. Decision: A structured plan with actionable recommendations."
        }

    async def check_auth(self) -> bool:
        return True

    async def agenerate(self, messages: List[Dict], temperature: Optional[float] = None) -> str:
        """A mock response from LLM, will respond based on the input message."""
        try:
            if not messages:
                return "Mock LLM: No message provided."

            for msg in messages:
                if "Plan" in msg["content"]:
                    return self.responses.get("plan", "Mock LLM response: Plan not found.")
                if "materials" in msg["content"].lower():
                    return self.responses.get("materials", "Mock LLM response: Materials not found.")
                if "strategies" in msg["content"].lower():
                    return self.responses.get("strategies", "Mock LLM response: Strategies not found.")
            return "Mock LLM response: No matching message found."
        except Exception as e:
            logging.error(f"Error in mock LLM: {e}")
            raise LLMError(f"Error in mock LLM: {e}")