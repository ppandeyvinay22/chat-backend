from flask import Flask
from flask_cors import CORS

from routes.chat_api import query_bp
from routes.update_api import update_bp

from services.scheduler_service import schedule_daily_updates

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(query_bp)
app.register_blueprint(update_bp)

# Start background scheduler
# schedule_daily_updates()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
