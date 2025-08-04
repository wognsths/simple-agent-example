import requests
import feedparser
from bs4 import BeautifulSoup
from langchain.tools import Tool
from typing import Tuple, List
from pydantic import BaseModel, Field

class NewsData(BaseModel):
    title: str
    link: str
    content: str

class NewsInputSchema(BaseModel):
    limit: int = Field(default=5, description="Number of news to fetch (Default 5)")

def _fetch_bbs_rss_links(limit: int = 5) -> List[Tuple[str, str]]:
    limit = int(limit)
    rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(rss_url)
    entries = feed.entries[:limit]
    return [(entry.title, entry.link) for entry in entries]

def _extract_article(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        
        paragraphs = soup.select("article div[data-component='text-block']")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return text if text else "Text not found"
    except Exception as e:
        return f"Error: {str(e)[:500]}"

def fetch_news_data(limit: int = 5) -> List[NewsData]:
    limit = int(limit)
    rss_links = _fetch_bbs_rss_links(limit)
    news_data = []
    for title, link in rss_links:
        article_text = _extract_article(link)
        news_data.append(NewsData(title=title, link=link, content=article_text))
    return news_data

def news_tool_func(limit: int = 5) -> str:
    limit = int(limit)
    news_items = fetch_news_data(limit=limit)

    return "\n\n".join(
        f"""📰 **{item.title}**
🔗 {item.link}
📄 {item.content.strip()}..."""
        for item in news_items
    )

news_tool = Tool(
    name="NewsTool",
    func=news_tool_func,
    description="Get the title, link, and content of the most recent news.",
    args_schema=NewsInputSchema
)