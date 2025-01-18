# shopy/models.py

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class State(BaseModel):
    query: str = Field(..., description="The user's query.")
    email: str = Field(..., description="The user's email address.")
    products: List[Dict[str, Any]] = Field(default_factory=list, description="List of products retrieved from search.")
    product_schema: List[Dict[str, Any]] = Field(default_factory=list, description="List of products with their schemas.")
    blogs_content: List[str] = Field(default_factory=list, description="Content from blogs related to products.")
    best_product: Optional[Dict[str, Any]] = Field(None, description="The best product selected after comparison.")
    comparison: List[Dict[str, Any]] = Field(default_factory=list, description="Comparison data between products.")
    youtube_link: str = Field("", description="Link to a YouTube review of the best product.")
    display_data: Dict[str, Any] = Field(default_factory=dict, description="Data to be displayed to the user.")
    summary: str = Field("", description="Summary of the products.")
    # Include any other fields as necessary