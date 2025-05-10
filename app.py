from flask import Flask
from flask_cors import CORS
import os

from routes.chat_api import query_bp
from routes.update_api import update_bp

# from services.scheduler_service import schedule_daily_updates
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(query_bp)
app.register_blueprint(update_bp)

# Start background scheduler
# schedule_daily_updates()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
