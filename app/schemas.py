from datetime import datetime
from optparse import Option
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    ## Config class tells FastAPI to automatically convert the ORM post object received 
    ## from SQLALchemy query to dictionary before sending the reponse via the deocrator response_model
    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr ## SecretStr converts password to asterisks during traceback or logging
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None