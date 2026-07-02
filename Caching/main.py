from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

# Cache storage
cache_data = []
last_fetch = 0
CACHE_TTL = 60  # seconds


@app.get("/news")
def get_news():
    global cache_data, last_fetch

    start = time.time()

    if time.time() - last_fetch > CACHE_TTL:
        print("Fetching fresh data...")

        url = "https://indianexpress.com/section/india/?ref=newlist_hp"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Create a fresh list
        news = []

        for h2 in soup.find_all("h2", class_="title"):
            news.append(h2.get_text(strip=True))

        # Replace old cache
        cache_data = news
        last_fetch = time.time()

    else:
        print("Using cached data")

    end = time.time()

    return {
        "time_taken": round(end - start, 4),
        "cached_at": last_fetch,
        "count": len(cache_data),
        "data": cache_data[:5]
    }