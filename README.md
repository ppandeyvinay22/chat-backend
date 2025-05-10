This is the backend service for a news-based chatbot. It fetches the latest news articles, embeds them using a SentenceTransformer model, stores them in ChromaDB for semantic search, and responds to queries using Google Gemini.

## Features

- Fetches news from a public RSS feed (BBC).
- Embeds articles using `all-MiniLM-L6-v2` via SentenceTransformer.
- Stores embeddings in ChromaDB (persistent vector store).
- Supports conversational querying using Google Gemini with semantic context.
- Stores user sessions and chat history in Redis (Upstash).
- Automatically clears sessions after 1 hour of inactivity.
- Background scheduler updates news daily.
- REST API endpoints for interacting with the chat system.

## Tech Stack

- Python 3.10+
- Flask
- ChromaDB
- SentenceTransformer
- Redis (Upstash)
- APScheduler
- Google Gemini API

## Setup Instructions

1. Clone the repository and navigate to the backend folder:

```bash
cd backend
