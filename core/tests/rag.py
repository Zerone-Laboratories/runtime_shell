from pymongo import MongoClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["runtime_db"]
collection = db["runtime_instruct"]

# Fetch documents from MongoDB
documents = []
for doc in collection.find({}):
    print(doc)  # Debugging: Check if data is retrieved correctly
    documents.append(doc["instructions"])

# Split text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splitted_docs = text_splitter.create_documents(documents)

# Initialize vector store with a collection name
vectorstore = Chroma(collection_name="runtime_collection", embedding_function=GPT4AllEmbeddings())

# Reset collection to avoid errors
vectorstore.reset_collection()

# Add processed documents to the collection
vectorstore.add_documents(splitted_docs)

# Search function
def search_runtime_docs(query, top_k=3):
    results = vectorstore.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]

# Example query
query = "How to install python"
search_results = search_runtime_docs(query)

# Print results
print("\nSearch Results:")
for idx, res in enumerate(search_results, 1):
    print(f"{idx}. {res}\n")
