import os
import json
from sentence_transformers import SentenceTransformer
import chromadb

# Path and chunk size for the data
CHROMA_DIR = "embeddings/news_db"
CHUNK_SIZE = 300

# Load the model once to be reused
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# Function for generating embeddings and storing in ChromaDB from the JSON data
def generate_embeddings_from_json():
    DATA_PATH = "data/bbc_news.json"

    os.makedirs("embeddings", exist_ok=True)

    with open(DATA_PATH, "r") as f:
        articles = json.load(f)

    docs = []
    metadatas = []
    for i, article in enumerate(articles):
        text = f"{article['title']}. {article['summary']}"
        for j in range(0, len(text), CHUNK_SIZE):
            chunk = text[j : j + CHUNK_SIZE]
            docs.append(chunk)
            metadatas.append({"source": f"article_{i}", "chunk": j // CHUNK_SIZE})

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs).tolist()

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_or_create_collection(name="news_articles")

    # Update if no data else add new one in the directory
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[f"doc_{i}" for i in range(len(docs))],
    )

    return {"message": f"Stored {len(docs)} chunks in ChromaDB"}


# Function for generating query embeddings and fetching relevant documents from ChromaDB
def generate_query_embeddings(query):
    try:
        # Embed the query
        query_embedding = embedder.encode([query]).tolist()

        # Initialize Chroma client
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = chroma_client.get_or_create_collection(name="news_articles")

        # Query ChromaDB for the top documents based on the query's embedding
        results = collection.query(query_embeddings=query_embedding, n_results=5)
        top_documents = results["documents"][0]

        return top_documents

    except Exception as e:
        return {"error": str(e)}
