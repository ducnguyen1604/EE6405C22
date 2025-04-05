from pydantic import BaseModel
from typing import List, Dict

class Product(BaseModel):
    id: int
    name: Dict[str, str]
    category: str
    price: float
    image: str
    description: Dict[str, str]
    rating: float
    comments: List[str]
