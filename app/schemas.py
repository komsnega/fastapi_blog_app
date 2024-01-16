from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
      title: str          
      content: str
      published: bool = True

class PostCreate(PostBase):
      pass

class UserResponse(BaseModel):
    user_id: int          
    email: EmailStr
    created_at: datetime

    class Config:
         from_attributes = True  

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
         from_attributes = True

class PostOut(BaseModel):
     post: PostResponse
     vote: int

     class Config:
          from_attributes = True    

class UserCreate(BaseModel):
     email: EmailStr
     password: str 

class UserLogin(BaseModel):
     email: EmailStr
     password: str
     
class Token(BaseModel):
     access_token : str
     token_type : str

class TokenData(BaseModel):
     id: Optional[str] = None

class Vote(BaseModel):
     post_id: int
     dir: Literal[0, 1]