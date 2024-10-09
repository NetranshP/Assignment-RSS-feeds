from celery import Celery
from database import NewsArticle, Session
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

app = Celery('news_processing', broker='pyamqp://guest:guest@localhost//')

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    words = word_tokenize(text)
    filtered_words = [ps.stem(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]
    return filtered_words

def categorize_article(article):
    terrorism_keywords = ['terrorism', 'protest', 'political unrest', 'riot', 'bomb']
    positive_keywords = ['positive', 'uplifting', 'inspiring']
    natural_disaster_keywords = ['natural disaster', 'earthquake', 'flood', 'hurricane']

    processed_content = preprocess_text(article['content'])

    processed_set = set(processed_content)

    if any(keyword in processed_content for keyword in terrorism_keywords):
        return 'Terrorism/Protest/Political Unrest/Riot'
    elif any(keyword in processed_content for keyword in positive_keywords):
        return 'Positive/Uplifting'
    elif any(keyword in processed_content for keyword in natural_disaster_keywords):
        return 'Natural Disasters'
    else:
        return 'Others'

@app.task
def process_article(article_id):
    session = Session()  
    article = session.query(NewsArticle).filter_by(id=article_id).first()
    if article:
        category = categorize_article(article)
        article.category = category
        session.commit()
