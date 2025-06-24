import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables from .env file

load_dotenv()

# 1. Verify API key is present

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found in .env file.")
print("API Key loaded.")

# 2. Initialize the Chat Model

try:

    chat = ChatOpenAI(temperature=0.7) 
    print("Chat Model initialized.")

except Exception as e:

    print(f"Error initializing model: {e}")
    exit()

# 3. Create and send a message

print("Sending message to the LLM...")

message = HumanMessage(

    content="In one sentence, why is learning about AI in 2024 important for a student?"

)

# 4. Receive and print the response

try:

    response = chat.invoke([message])
    print("\n--- AI Response ---")
    print(response.content)
    print("-------------------\n")

except Exception as e:

    print(f"Error during API call: {e}")
