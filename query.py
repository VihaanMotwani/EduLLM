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
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 1. Load the existing index from the vector store
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("EduLLM_RAG")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# 2. Create a query engine
query_engine = index.as_query_engine(similarity_top_k=3)

question = input("User: ")

response = query_engine.query(question)
print(response)

print("--- Source Nodes ---")
for node in response.source_nodes:
    print(node.get_content())