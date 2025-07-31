import os
import time
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.packs.raptor import RaptorPack, RaptorRetriever
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import qdrant_client
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_PATH = os.path.join(PROJECT_ROOT, "docs")
QDRANT_PATH = os.path.join(PROJECT_ROOT, "backend", "qdrant_db")

class RaptorService:
    """
    A service class to manage the RAPTOR RAG pipeline using Qdrant,
    which correctly handles the data structure.
    """
    def __init__(self, force_rebuild=False, collection_name="edullm_raptor_qdrant"):
        print("Initializing RaptorService with Qdrant...")
        self.collection_name = collection_name
        
        # --- Qdrant Client and Vector Store Setup ---
        # Connect to Qdrant server instead of local file
        self.client = qdrant_client.QdrantClient(host="localhost", port=6333)
        self.aclient = AsyncQdrantClient(host="localhost", port=6333)
        
        # Check if we need to rebuild
        # A simple way is to check if the collection exists and force_rebuild is True
        try:
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            if force_rebuild:
                print(f"Force rebuilding collection: {self.collection_name}")
                self.client.delete_collection(collection_name=self.collection_name)
                raise Exception("Rebuilding") # Force exception to enter the build block
        except Exception:
             print("Database is empty or rebuilding. Building new RAPTOR index...")
             if not os.path.exists(DATA_PATH) or not os.listdir(DATA_PATH):
                 raise ValueError("Data directory is empty. Please add documents before building.")
             
             # Pass both sync and async clients to QdrantVectorStore
             self.vector_store = QdrantVectorStore(
                 client=self.client,
                 aclient=self.aclient,
                 collection_name=self.collection_name
             )
             self.documents = SimpleDirectoryReader(DATA_PATH).load_data()
             self._build_raptor_tree()
        else:
            print("Loading existing RAPTOR index from Qdrant.")
            self.vector_store = QdrantVectorStore(
                client=self.client,
                aclient=self.aclient,
                collection_name=self.collection_name
            )
            self._load_retriever()

    def _build_raptor_tree(self):
        """Builds the RAPTOR index in Qdrant."""
        print("Creating RaptorPack and building the tree...")
        raptor_pack = RaptorPack(
            self.documents,
            embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1),
            vector_store=self.vector_store,
            similarity_top_k=2,
            mode="collapsed",
            verbose=True
        )
        self.retriever = raptor_pack.get_modules()["retriever"]
        print("RAPTOR tree built successfully in Qdrant.")

    def _load_retriever(self):
        """Loads an existing retriever from the Qdrant vector store."""
        print("Setting up RaptorRetriever from existing Qdrant index...")
        self.retriever = RaptorRetriever(
            [],
            embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1),
            vector_store=self.vector_store,
            similarity_top_k=2,
            mode="collapsed",
        )
        print("RaptorRetriever loaded successfully from Qdrant.")

# --- Helper Function for Agent Service ---
def get_raptor_retriever():
    service = RaptorService()
    return service.retriever

if __name__ == "__main__":
    print("Running ingestion script for Qdrant...")
    start_time = time.time()
    RaptorService(force_rebuild=True)
    end_time = time.time()
    print(f"Ingestion completed in {end_time - start_time:.2f} seconds.")