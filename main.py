__name__ = "__main__"
import feedparser
from datetime import datetime
from urllib.parse import urlparse
import hashlib
from hashlib import sha256
from celery_worker import process_article  
from database import NewsDatabase

feeds = [
  'http://rss.cnn.com/rss/cnn_topstories.rss',
  'http://qz.com/feed',
  'http://feeds.foxnews.com/foxnews/politics',
  'http://feeds.reuters.com/reuters/businessNews',
  'http://feeds.feedburner.com/NewshourWorld',
  'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml',
]


def parse_feed(feed_url):
    parsed_articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
       
        pub_date = (
            datetime(*entry.published_parsed[:6])
            if hasattr(entry, 'published_parsed')
            else datetime.now()  
        )

        content = entry.summary if 'summary' in entry else entry.description if 'description' in entry else ''
    
        article = {
            'id': hashlib.sha256((entry.title + entry.link).encode()).hexdigest(),
            'title': entry.title,
            'content': content,
            'pub_date': pub_date,
            'source_url': entry.link,
        }
        parsed_articles.append(article)
    return parsed_articles

all_articles = []
for feed_url in feeds:
    all_articles.extend(parse_feed(feed_url))


unique_articles = {hashlib.sha256(article['title'].encode() + article['source_url'].encode()).hexdigest(): article for article in all_articles}.values()

news_db = NewsDatabase()

for article in unique_articles:
    news_db.insert_article(article)
    print(f"Submitting task for article ID: {article['id']}")
    process_article.delay(article['id'])
