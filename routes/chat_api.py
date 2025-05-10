import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from redis_client import redis_client
from services.embedding_service import generate_query_embeddings
from services.gemini_service import generate_answer
from functools import wraps

query_bp = Blueprint("query_bp", __name__, url_prefix="/api")

# session timout for 1 hour
SESSION_TTL = 3600


# Decorator to check if session exists in Redis
def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        session_id = data.get("session_id")
        if not session_id or not redis_client.exists(f"user:{session_id}"):
            return (
                jsonify(
                    {"error": "Session expired or invalid. Please start a new session."}
                ),
                401,
            )
        return func(*args, **kwargs)

    return wrapper


# API 1: Create a new session
@query_bp.route("/create_user_session", methods=["POST"])
def create_user_session():
    try:
        session_id = str(uuid.uuid4())
        session_data = {"timestamp": datetime.utcnow().isoformat(), "data": []}
        redis_client.setex(f"user:{session_id}", SESSION_TTL, json.dumps(session_data))
        return jsonify({"session_id": session_id}), 200
    except Exception as e:
        print("error in create user session api:", e)
        return jsonify({"error": "Internal Server error"}), 500


# API 2: Handle query (modified)
@query_bp.route("/query", methods=["POST"])
@check_session
def handle_query():
    data = request.get_json()
    session_id = data.get("session_id")
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        top_documents = generate_query_embeddings(query)

        if not top_documents:
            return jsonify({"answer": "No relevant context found."}), 200

        context = "\n\n".join(top_documents[:2])
        answer = generate_answer(f"Context:\n{context}\n\nQuery: {query}")

        # Update session data in Redis
        session_key = f"user:{session_id}"
        session_data = json.loads(redis_client.get(session_key))
        # print("old sesion data:", session_data)
        session_data["data"].append({"question": query, "answer": answer})
        session_data["timestamp"] = (datetime.utcnow().isoformat(),)
        # print("new session data:", session_data)
        redis_client.setex(session_key, SESSION_TTL, json.dumps(session_data))

        return jsonify({"question": query, "answer": answer}), 200
    except Exception as e:
        print("error in api/query api:", e)
        return jsonify({"error": "Internal Server error"}), 500


# API 3: Get full session history
@query_bp.route("/get_session_history", methods=["POST"])
@check_session
def get_session_history():
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        session_key = f"user:{session_id}"
        session_data = json.loads(redis_client.get(session_key))
        return jsonify({"history": session_data}), 200
    except Exception as e:
        print("error in get session history api:", e)
        return jsonify({"error": "Internal Server error"}), 500


# API 4: Clear session manually
@query_bp.route("/clear_session", methods=["POST"])
def clear_session():
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        session_key = f"user:{session_id}"
        redis_client.delete(session_key)
        return jsonify({"message": "Session cleared successfully."}), 200
    except Exception as e:
        print("error in clear session api:", e)
        return jsonify({"error": "Internal Server error"}), 500
