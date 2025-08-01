from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agent

app = FastAPI()

# CORS config
# List of allowed origins (your frontend's URL)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],      # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],      # Allows all headers
)

app.include_router(agent.router, prefix="/agent", tags=["Agent"])

@app.get("/")
def read_root():
    return {"Hello": "World"}