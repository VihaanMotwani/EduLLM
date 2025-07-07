import os
from dotenv import load_dotenv
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
#pip install llama-index-vector-stores-chroma
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

load_dotenv()
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

print("Loading documents from './data' directory...")

reader = SimpleDirectoryReader("./data")
documents = reader.load_data()
print(f"Loaded {len(documents)} document(s).")

print("Initializing ChromaDB...")
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("EduLLM_RAG")
print("ChromaDB collection created/loaded.")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
print("Vector store and storage context defined.")

print("Creating the index.")
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=20)]
)
print("Index creation complete. You can now query your data.")


