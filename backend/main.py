import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List

# --- Local Imports ---
import db_utils
import auth_utils
from pydantic_models import QueryInput, QueryResponse, UserCreate, User, Token, Chat
from langgraph_agent import agent # Assuming your agent is ready
from langchain_core.messages import HumanMessage
from langchain_utils import contextualise_chain
from utils import history_to_lc_messages, append_message

app = FastAPI()

# --- CORS Middleware ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AUTHENTICATION ENDPOINTS

@app.get("/")
def read_root():
    return {"message": "Welcome to the EduLLM API"}

@app.post("/register", response_model=User)
def register_user(user: UserCreate):
    db_user = db_utils.get_user(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth_utils.get_password_hash(user.password)
    user_id = db_utils.add_user(username=user.username, hashed_password=hashed_password)
    if user_id is None:
        raise HTTPException(status_code=500, detail="Could not create user")
    return User(id=user_id, username=user.username)

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_utils.get_user(username=form_data.username)
    if not user or not auth_utils.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# CHAT ENDPOINTS

@app.get("/chats", response_model=List[Chat])
def get_user_chat_list(current_user: User = Depends(auth_utils.get_current_user)):
    """Retrieves all chat threads for the logged-in user."""
    return db_utils.get_user_chats(user_id=current_user.id)

@app.post("/chats", response_model=Chat)
def create_new_chat(current_user: User = Depends(auth_utils.get_current_user)):
    """Creates a new, empty chat thread for the logged-in user."""
    # Use a default title; the user can rename it later.
    new_chat_id = db_utils.create_chat(user_id=current_user.id, title="New Chat")
    new_chat = db_utils.get_chat(chat_id=new_chat_id) # Assumes you create a `get_chat` function
    return new_chat

@app.get("/chats/{chat_id}/messages")
def get_chat_history(chat_id: int, current_user: User = Depends(auth_utils.get_current_user)):
    """Retrieves the message history for a specific chat."""
    owner_id = db_utils.get_chat_owner(chat_id)
    if owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this chat")
    return db_utils.get_chat_messages(chat_id=chat_id)


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput, current_user: User = Depends(auth_utils.get_current_user)):
    """
    Main chat endpoint, now protected and linked to a user and chat_id.
    """
    # 1. Verify that the user owns the chat they are trying to post to
    owner_id = db_utils.get_chat_owner(query_input.chat_id)
    if owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to post to this chat")

    # 2. Add the user's message to the database
    db_utils.add_message_to_history(query_input.chat_id, "human", query_input.question)

    # 3. Get the full chat history for context
    chat_history = db_utils.get_chat_messages(query_input.chat_id)
    messages = history_to_lc_messages(chat_history)
    
    # 4. Generate a standalone question (Contextualization)
    standalone_q = contextualise_chain.invoke({
        "chat_history": messages[:-1], # Pass history *before* the current question
        "input": query_input.question,
    })

    # 5. Invoke the agent
    result = agent.invoke({"messages": [HumanMessage(content=standalone_q)]})
    answer = result["messages"][-1].content
    
    # 6. Save the AI's response to the database
    db_utils.add_message_to_history(query_input.chat_id, "ai", answer)

    return QueryResponse(answer=answer, chat_id=query_input.chat_id, model=query_input.model)