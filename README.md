# EduLLM - Your Personal AI/ML Tutor

Welcome to the EduLLM project! This is an AI-powered tutor for Artificial Intelligence, Machine Learning and related topics.

## 🤖 Core Architecture

The application is built with a modern, full-stack architecture:

* **Frontend:** A responsive chat interface built with **React**.
* **Backend:** A powerful API built with **Python FastAPI**.
* **AI Agent:** An intelligent, stateful agent orchestrated with **LangGraph**.
* **Knowledge Base (RAG):** The agent can retrieve information from a custom knowledge base using an advanced **RAPTOR** indexing strategy, powered by **LlamaIndex** and a **Qdrant** vector database.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* Python (3.10+)
* Node.js and npm
* Git

You will also need an **OpenAI API Key**.

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd EduLLM
```

### 2. Backend Setup

First, let's set up the Python backend and the knowledge base.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate
# On Windows, use: venv\Scripts\activate

# Install the required Python dependencies
pip install -r requirements.txt

# Create the environment file for your API key
cp .env.example .env
```

Now, open the newly created `.env` file and add your OpenAI API Key:

```env
OPENAI_API_KEY="your_api_key_here"
```

### 3. Build the Knowledge Base

The agent's knowledge comes from the documents in the `/data` directory. You must run the ingestion script once to build the vector database.

```bash
# From the backend directory (with your venv active)
python -m services.rag_service
```

This will create a `qdrant_db` folder in the backend.

### 4. Frontend Setup

Now, let's set up the React user interface. Open a **new terminal** for this.

```bash
# Navigate to the frontend directory from the project root
cd frontend

# Install the required npm packages
npm install
```

### 5. Running the Application

To run the full application, you need to have **two terminals** running simultaneously.

* **Terminal 1: Start the Backend**
    ```bash
    # In the /backend directory with venv active
    uvicorn main:app --reload
    ```

* **Terminal 2: Start the Frontend**
    ```bash
    # In the /frontend directory
    npm start
    ```

Your application should now be running! The frontend will be accessible at `http://localhost:3000`.

## 📂 Project Structure

A brief overview of the key directories:

* `/data`: Contains the raw `.pdf` and `.md` files for the RAG knowledge base.
* `/frontend`: The React application for the user interface.
* `/backend`: The FastAPI application.
    * `/routers`: Defines the API endpoints.
    * `/services`: Contains the core AI logic (agent and RAG services).
    * `/qdrant_db`: The local vector database (created after ingestion).

## 🤝 How to Contribute

1.  Create a new branch for your feature (e.g., `feature/add-user-auth`).
2.  Make your changes and commit them with clear, descriptive messages.
3.  Push your branch to the repository and open a Pull Request.