# shopy/exceptions.py

class TavilySearchError(Exception):
    """Custom exception for Tavily search errors."""
    def __init__(self, message: str):
        super().__init__(message)

class DataStructuringError(Exception):
    """Custom exception for data structuring errors."""
    def __init__(self, message: str):
        super().__init__(message)

class ProductComparisonError(Exception):
    """Custom exception for product comparison errors."""
    def __init__(self, message: str):
         super().__init__(message)

class YouTubeReviewError(Exception):
    """Custom exception for YouTube review errors."""
    def __init__(self, message: str):
        super().__init__(message)

class LLMError(Exception):
    """Custom exception for LLM errors."""
    def __init__(self, message: str):
         super().__init__(message)

class EmailError(Exception):
    """Custom exception for email sending errors."""
    def __init__(self, message: str):
        super().__init__(message)