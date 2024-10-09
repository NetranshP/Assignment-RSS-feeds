## News Classification System
The News Classification System is designed to retrieve news articles from multiple RSS feeds, parse them, eliminate duplicates, and classify them into specific categories using a Celery worker for asynchronous processing. PostgreSQL serves as the database to store the news articles and their corresponding categories.
News-Classification-

1) main.py                  # Main script responsible for fetching, parsing, and handling news articles
2) celery_worker.py         # Celery worker for asynchronous classification and processing
3) database.py              # Database schema and methods for database interactions
4) README.md                # Documentation for the project

## Components

main.py:

Functions:
Fetches news articles from various RSS feeds.
Parses the articles and stores them in the database.
Ensures there are no duplicate articles by comparing title and source URL.
Key Modules:
feedparser: For parsing RSS feeds.
datetime: For managing date and time.
urllib.parse: To parse URLs.
hashlib: To generate secure hashes for comparison.
celery_worker.process_article: An asynchronous task to handle classification.
database.NewsDatabase: Manages database interactions.

database.py:

Role:
Defines the SQLAlchemy model for the NewsArticle table.
Provides a session interface (NewsDatabase) to manage interactions with the database.
Dependencies:
sqlalchemy: ORM and SQL toolkit.

celery_worker.py:

Role:
Contains the Celery task (process_article) for categorizing articles asynchronously.
Handles the article classification logic using NLP techniques directly in this file.
Modules Used:
celery: Distributed task queue for managing asynchronous tasks.
nltk: Natural Language Processing toolkit for text processing.
database.NewsArticle: References the article model for database integration.
Contains text preprocessing, tokenization, stop word removal, and categorization.

Design Highlights

Asynchronous Processing:
Uses Celery to handle time-consuming tasks like text classification in the background, enhancing responsiveness and scalability.

Database Design:
PostgreSQL is chosen for its robustness in handling relational data.
The NewsArticle model consists of fields such as id, title, content, pub_date, source_url, and category for classifying articles.

Text-Based Categorization:
Basic Natural Language Processing is utilized for classifying articles into predefined categories based on keyword analysis.
Articles that match certain positive keywords are placed in an "Uplifting" category, while other articles fall into the "Others" category.

Duplicate Detection:
Duplicate articles are filtered by generating a unique hash using the title and source URL, ensuring no redundant storage.

Output
The system generates a CSV file containing processed articles, including fields like id, title, content, pub_date, source_url, and category.
