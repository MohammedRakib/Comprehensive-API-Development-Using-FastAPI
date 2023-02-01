from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP
from pydantic import BaseModel
from typing import Optional
from .database import Base

class PostDB(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(45), nullable=False)
    content = Column(String(60), nullable=False)
    published = Column(Boolean, server_default=text('TRUE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    