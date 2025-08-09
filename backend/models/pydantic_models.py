from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

# --- Chat Models ---

class ModelName(str, Enum):
    GPT4_1 = "gpt-4.1"
    GPT4_1_MINI = "gpt-4.1-mini"

class QueryInput(BaseModel):
    question: str
    chat_id: int
    model: ModelName = Field(default=ModelName.GPT4_1_MINI)

class QueryResponse(BaseModel):
    answer: str
    chat_id: int
    model: ModelName

class Chat(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatUpdate(BaseModel):
    title: str

# --- User & Authentication Models ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None