import os
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.packs.raptor import RaptorPack
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.packs.raptor.base import SummaryModule
import chromadb
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_PATH = os.path.join(PROJECT_ROOT, "test_data")
CHROMA_PATH = os.path.join(PROJECT_ROOT, "backend", "raptor_db")

def get_raptor_retriever():
    """
    Initializes and returns a RaptorRetriever using monkey-patching to
    control the number of clusters.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data directory not found at: {DATA_PATH}")

    db = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = db.get_or_create_collection("raptor_patched_final")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    if chroma_collection.count() > 0:
        print("Loading existing RAPTOR index from ChromaDB.")
        raptor_pack = RaptorPack([], vector_store=vector_store)
    else:
        print("Building new RAPTOR index with patched clustering...")
        documents = SimpleDirectoryReader(DATA_PATH).load_data()

        summary_module = SummaryModule(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1),
            summary_prompt="As a professional summarizer, create a concise, comprehensive, and detailed summary of the provided text.",
            num_workers=8, # Adjust based on your machine and API rate limits
        )

        raptor_pack = RaptorPack(
            documents,
            embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1),
            vector_store=vector_store,
            summary_module=summary_module,
            verbose=True
        )
        print(f"Successfully built RAPTOR index for {len(documents)} documents.")

    return raptor_pack.get_modules()["retriever"]

if __name__ == "__main__":
    print("Building RAPTOR vector store index...")
    get_raptor_retriever()
    print("RAPTOR vector store index built successfully.")