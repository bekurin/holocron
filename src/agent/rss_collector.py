import requests
import feedparser
import time
from datetime import datetime, timedelta
from typing import List
from model.news_information import NewsInformation
from util.contant import GOOGLE_RSS_URL


class RssCollectorAgent:
    def run(self, company_name: str, limit: int = 15) -> List[NewsInformation]:
        """kospi 100 당일 기사 내용 검색"""
        url = GOOGLE_RSS_URL.format(query=company_name)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        feed = feedparser.parse(response.text)

        today = datetime.now().date()
        news_list: List[NewsInformation] = []

        for entry in feed.entries[:limit]:
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6]).date()

                if published_date == today:
                    news = NewsInformation()
                    news.title = entry.title
                    news.link = entry.link
                    news.published = entry.published_parsed
                    news_list.append(news)
        return news_list
