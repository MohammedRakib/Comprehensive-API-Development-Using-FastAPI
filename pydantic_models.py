from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    body: str
    published: bool = True
    rating: Optional[int] = None