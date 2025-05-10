from apscheduler.schedulers.background import BackgroundScheduler
from services.rss_service import fetch_rss_articles
from services.embedding_service import generate_embeddings_from_json


def run_news_update():
    try:
        print("Running daily news update...")
        rss_result = fetch_rss_articles()
        embed_result = generate_embeddings_from_json()
        print("ran schedulder")
        return {"response": "Success"}
    except Exception as e:
        print(f"Error in scheduled update: {e}")
        return {"response": str(e)}


def schedule_daily_updates():
    scheduler = BackgroundScheduler()

    # Schedule job every 24 hours
    scheduler.add_job(func=run_news_update, trigger="interval", days=1)

    scheduler.start()
