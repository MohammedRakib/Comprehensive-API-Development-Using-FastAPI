from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP
from .database import Base

class PostDB(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(45), nullable=False)
    content = Column(String(60), nullable=False)
    published = Column(Boolean, server_default=text('TRUE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    
    

    