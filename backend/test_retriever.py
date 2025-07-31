# in backend/test_retriever.py

from services.rag_service import get_raptor_retriever
import time

def manual_test():
    """
    A simple script to manually test the retriever with user input.
    """
    print("--- Initializing Retriever (loading from Qdrant)... ---")
    start_time = time.time()
    
    # This loads your existing, pre-built index
    retriever = get_raptor_retriever()
    
    end_time = time.time()
    print(f"--- Retriever loaded in {end_time - start_time:.2f} seconds. ---")

    # Loop to allow for multiple test queries
    while True:
        print("\n" + "="*50)
        query = input("Enter your test query (or type 'exit' to quit): ")
        
        if query.lower() == 'exit':
            break
            
        print(f"\nSearching for: '{query}'...")
        start_time = time.time()
        
        retrieved_docs = retriever.retrieve(query)
        
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.2f} seconds.")

        if retrieved_docs:
            print(f"\nSUCCESS: Found {len(retrieved_docs)} documents.")
            for i, doc in enumerate(retrieved_docs):
                print(f"\n--- Document {i+1} (Score: {doc.score:.4f}) ---")
                print(doc.get_content()[:300] + "...") # Print a snippet
        else:
            print("\nFAILURE: No documents were found for this query.")

if __name__ == "__main__":
    manual_test()