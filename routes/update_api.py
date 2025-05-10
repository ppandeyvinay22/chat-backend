from flask import Blueprint, jsonify
from services.rss_service import fetch_rss_articles
from services.embedding_service import generate_embeddings_from_json

update_bp = Blueprint("update_bp", __name__, url_prefix="/api")


@update_bp.route("/update-data", methods=["POST"])
def update_all():
    try:
        rss_result = fetch_rss_articles()
        embed_result = generate_embeddings_from_json()
        return jsonify({"message": "Successfully updated data with latest news!"}), 200
    except Exception as e:
        print("error in update news api:", e)
        return jsonify({"error": "Internal Server error"}), 500
