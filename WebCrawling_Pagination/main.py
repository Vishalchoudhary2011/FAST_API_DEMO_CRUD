from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_news(page:int = 1,limit:int = 5):
    url = "https://indianexpress.com/section/india/?ref=newlist_hp"

    response =  requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = []
    for h2 in soup.find_all("h2", class_="title"):
        title.append(h2.get_text(strip=True))

    #Pagination logic
    start = (page -1)* limit    
    end = start+limit
        
    return {
        "page": page,
        "limit": limit,
        "total": len(title),
        "data": title[start:end]
    }
