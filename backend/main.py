import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse
from db_utils import insert_chat_history, get_chat_history
from langgraph_agent import agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import logging
from utils import get_or_create_session_id, history_to_lc_messages, append_message
from langchain_utils import contextualise_chain
logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()

origins = [
    # The origin of your React frontend
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# Load environment variables from .env file
load_dotenv(override=True)

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    """
    Main chat endpoint using the LangGraph agent with routing, RAG, and web search capabilities.
    """
    session_id = get_or_create_session_id(query_input.session_id)
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

    try:
        # Convert chat history to LangChain messages
        chat_history = get_chat_history(session_id)
        messages = history_to_lc_messages(chat_history)
        # Add current user message

                # 2. Generate a stand-alone question
        standalone_q = contextualise_chain.invoke({
            "chat_history": messages,
            "input": query_input.question,
        })

        messages = append_message(messages, HumanMessage(content=standalone_q))
        # Invoke the LangGraph agent
        # config = {"configurable": {"thread_id": session_id}}
        result = agent.invoke(
            {"messages": messages}
        )

        # Get the last AI message
        last_message = next((m for m in reversed(result["messages"])
                           if isinstance(m, AIMessage)), None)

        if last_message:
            answer = last_message.content
        else:
            answer = "I apologize, but I couldn't generate a response at this time."

        # Store the conversation
        insert_chat_history(session_id, query_input.question, answer, query_input.model.value)
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")

        return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

    except Exception as e:
        logging.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")