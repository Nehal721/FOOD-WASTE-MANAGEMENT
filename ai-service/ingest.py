import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Paths
DATA_DIR = "data"
VECTOR_DB_DIR = "vector_db"

def load_documents():
    documents = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, file)
            print(f"Loading {file_path}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents

def main():
    print("Starting ingestion...")

    # 1. Load PDFs
    documents = load_documents()
    print(f"Loaded {len(documents)} pages")

    # 2. Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks")

    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Store in FAISS vector DB
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_DIR)

    print("✅ Vector database created successfully!")

if __name__ == "__main__":
    main()
