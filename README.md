# EduLLM - Your Personal AI/ML Tutor

Welcome to the EduLLM project! This is a scalable learning platform designed to act as an AI-powered tutor for Machine Learning and related topics.

## 🤖 Core Architecture

The application is built with a modern, full-stack architecture:

* **Frontend:** A responsive chat interface built with **React**.
* **Backend:** A powerful API built with **Python FastAPI**.
* **AI Agent:** An intelligent, stateful agent orchestrated with **LangGraph**.
* **Knowledge Base (RAG):** The agent can retrieve information from a custom knowledge base using an advanced **RAPTOR** indexing strategy, powered by **LlamaIndex** and a **Qdrant** vector database server.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* Python (3.10+)
* Node.js and npm
* Git

You will also need an **OpenAI API Key**.

## 🚀 Getting Started

Follow these steps in order to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd EduLLM
```

### 2. Backend & Database Setup

This section covers setting up the Python backend and the Qdrant vector database.

#### **Step 2a: Run the Qdrant Database Server**

Our RAG system requires a running Qdrant server. For local development, you will need to run a Qdrant instance.

Please refer to the **official Qdrant documentation** for instructions on how to install and run a local Qdrant server. This is often done by downloading a binary or using a package manager.

Once started, the Qdrant server should be accessible at `http://localhost:6333`.

#### **Step 2b: Set Up the Python Backend**

Now, let's set up the FastAPI application.

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

### 3. Build the Knowledge Base (Indexing)

The agent's knowledge comes from the documents in the `/data` directory. You must run the ingestion script once to populate the Qdrant database. This process reads your documents, chunks them, and creates a searchable index.

**Important:** Make sure your local Qdrant server is running before you execute this command.

```bash
# From the /backend directory (with your venv active)
python -m services.rag_service
```

This script will connect to your local Qdrant server and build the index.

### 4. Frontend Setup

Now, let's set up the React user interface. Open a **new terminal** for this.

```bash
# Navigate to the frontend directory from the project root
cd frontend

# Install the required npm packages
npm install
```

### 5. Running the Application

To run the full application, you need to have **three services** running: the Qdrant server, the backend, and the frontend.

* **Service 1: Qdrant Server**
    * This should be running based on your setup from Step 2a.

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

## 🤝 How to Contribute

1.  Create a new branch for your feature (e.g., `feature/add-user-auth`).
2.  Make your changes and commit them with clear, descriptive messages.
3.  Push your branch to the repository and open a Pull Request for review. Direct pushes to the `main` branch are disabled.
