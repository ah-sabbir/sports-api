from fastapi import FastAPI
import requests as req
from bs4 import BeautifulSoup as bs
import json

app = FastAPI()

espncricinfo_url = "https://www.espncricinfo.com"

@app.get("/", tags=["Root"])
async def read_root():
  return [ {
        "live_url": espncricinfo_url+a['href'],
        "title":a.find("div",{"class":"description"}).text,
        "team1": {
            "name": str(a.find("div",{"class":"teams"}).find_all("div",{"class":"team"})[0].find("div",{"class":"name-detail"}).text),
            "score": str(a.find("div",{"class":"teams"}).find_all("div",{"class":"team"})[0].find("div",{"class":"score-detail"})),
        },
        "team2": a.find("div",{"class":"teams"}).find_all("div",{"class":"team"})[-1].text,
        "status_text": a.find("div",{"class":"status-text"}).text,

            } for a in bs(req.get("https://www.espncricinfo.com/live-cricket-score").text,"lxml").find_all("a",{"class":"match-info-link-FIXTURES"})
         ]