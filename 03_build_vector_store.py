import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Define the path for the scraped data and the vector store
DATA_PATH = "data/scraped_data.txt"
DB_FAISS_PATH = "vectorstore/db_faiss"

def create_vector_db():
    """
    Creates a FAISS vector database from the scraped text data.
    """
    # 1. Load the data
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        print("Please run the scraper scripts first.")
        return
        
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    print("✅ 1/4: Data loaded successfully.")

    # 2. Chunk the data
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(raw_text)
    print(f"✅ 2/4: Text split into {len(chunks)} chunks.")

    # 3. Define the embedding model
    # We'll use a popular, efficient model from Hugging Face
    embeddings_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'} # Use CPU for broad compatibility
    )
    print("✅ 3/4: Embedding model loaded.")

    # 4. Create the FAISS vector store and save it
    # This will download the model from Hugging Face the first time you run it
    print("⏳ 4/4: Creating and saving the vector store... This may take a moment.")
    db = FAISS.from_texts(chunks, embeddings_model)
    db.save_local(DB_FAISS_PATH)
    
    print("---" * 20)
    print(f"✅ Vector store created and saved successfully at {DB_FAISS_PATH}")
    print("---" * 20)


if __name__ == "__main__":
    create_vector_db()