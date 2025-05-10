import redis
import os
from dotenv import load_dotenv

load_dotenv()
# Read REDIS_URL from env
REDIS_URL = os.getenv("REDIS_URL")
# print("redis url in redis client page:", REDIS_URL)

# Initialize Redis client using the URL
redis_client = redis.from_url(REDIS_URL, decode_responses=True)
