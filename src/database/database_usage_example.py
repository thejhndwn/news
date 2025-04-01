import os
import time
import schedule
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError

# Import our database modules
from database import init_db, Session
from models import Article, ScrapeJob

# Environment configuration
ENV = os.environ.get('ENV', 'development')
SCRAPE_INTERVAL = int(os.environ.get('SCRAPE_INTERVAL', '3600'))

# List of news sources to scrape (example)
NEWS_SOURCES = [
    {"name": "Example News", "url": "https://example.com/news"}
]

def record_job_start():
    """Record the start of a scraping job using SQLAlchemy"""
    session = Session()
    try:
        job = ScrapeJob(status='running')
        session.add(job)
        session.commit()
        return job.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error recording job start: {e}")
        return None
    finally:
        session.close()

def record_job_completion(job_id, articles_found, articles_saved):
    """Record the completion of a scraping job using SQLAlchemy"""
    if job_id is None:
        return
        
    session = Session()
    try:
        job = session.query(ScrapeJob).get(job_id)
        if job:
            job.end_time = datetime.now()
            job.status = 'completed'
            job.articles_found = articles_found
            job.articles_saved = articles_saved
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error recording job completion: {e}")
    finally:
        session.close()

def save_article(title, url, content, published_date, source):
    """Save article to the database using SQLAlchemy if it doesn't exist"""
    session = Session()
    try:
        # Check if article with this URL already exists
        existing = session.query(Article).filter(Article.url == url).first()
        if existing:
            return False
            
        # Create new article
        article = Article(
            title=title,
            url=url,
            content=content,
            published_date=published_date,
            source=source
        )
        session.add(article)
        session.commit()
        return True
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error saving article: {e}")
        return False
    finally:
        session.close()

def scrape_news():
    """Main function to scrape news from all sources"""
    print(f"Starting news scraping job at {datetime.now()} in {ENV} environment")
    
    job_id = record_job_start()
    articles_found = 0
    articles_saved = 0
    
    for source in NEWS_SOURCES:
        try:
            # This is a placeholder for your actual scraping logic
            # In a real implementation, you would parse the HTML and extract articles
            response = requests.get(source['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example article extraction (modify for your target site)
            articles = soup.find_all('article')
            articles_found += len(articles)
            
            for article in articles:
                # Extract article details (modify for actual HTML structure)
                title_elem = article.find('h2')
                link_elem = article.find('a')
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    url = link_elem.get('href')
                    
                    # Get article content (you'd need to fetch the article page)
                    content = "Article content here..."
                    published_date = datetime.now()  # You'd extract this from the article
                    
                    # Save to database
                    if save_article(title, url, content, published_date, source['name']):
                        articles_saved += 1
        
        except Exception as e:
            print(f"Error scraping {source['name']}: {e}")
    
    record_job_completion(job_id, articles_found, articles_saved)
    print(f"Completed job {job_id}: Found {articles_found} articles, saved {articles_saved} new articles")

def main():
    """Set up the database and run the scraper"""
    # Initialize the database
    print("Initializing database...")
    init_db()
    print("Database initialized successfully")
    
    # Run once immediately
    scrape_news()
    
    # Schedule to run at the specified interval
    schedule.every(SCRAPE_INTERVAL).seconds.do(scrape_news)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Allow some time for the database to start up
    time.sleep(5)
    main()