import os
import feedparser
import json
import traceback

def fetch_rss_articles():
    os.makedirs("data", exist_ok=True)
    rss_url = "http://feeds.bbci.co.uk/news/rss.xml"

    try:
        feed = feedparser.parse(rss_url)

        if not feed.entries:
            raise ValueError("No articles found in the feed.")

        articles = [{"title": entry.title, "summary": entry.summary} for entry in feed.entries]

        with open("data/bbc_news.json", "w") as f:
            json.dump(articles, f, indent=2)

        return {"message": f"Fetched {len(articles)} articles"}
    except Exception as e:
        error_msg = f"Error: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        with open("data/error.txt", "w") as f:
            f.write(error_msg)
        raise RuntimeError("Failed to fetch RSS data")
