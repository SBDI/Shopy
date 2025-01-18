# shopy/config.py

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    """A class to load and manage configuration settings from environment variables."""
    def __init__(self):
        # Construct the path to the .env file
        env_path = Path(__file__).resolve().parent.parent / ".env"  # Corrected path

        config_vars = {}
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config_vars[key.strip()] = value.strip()
                        #logging.debug(f"Loaded {key.strip()}={value.strip()} from .env")
        except FileNotFoundError:
            logging.error(f"Error: .env file not found at {env_path}")
            raise
        except Exception as e:
            logging.error(f"Error loading .env file: {e}")
            raise

        self.gmail_user = config_vars.get("GMAIL_USER")
        self.gmail_pass = config_vars.get("GMAIL_PASS")
        self.youtube_api_key = config_vars.get("YOUTUBE_API_KEY")
        self.tavily_api_key = config_vars.get("TAVILY_API_KEY")
        self.google_api_key = config_vars.get("GOOGLE_API_KEY")


        self._validate_config()

    def _validate_config(self):
        """Validates that required environment variables are set."""
        if not (self.google_api_key or (self.gmail_user and self.gmail_pass and self.youtube_api_key and self.tavily_api_key)):
             raise EnvironmentError(
                "Missing required environment variables. Please set either GROQ_API_KEY, GOOGLE_API_KEY or GMAIL_USER, GMAIL_PASS, YOUTUBE_API_KEY, and TAVILY_API_KEY."
            )