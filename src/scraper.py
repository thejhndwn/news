import logging
from database.database import init_db, get_engine
from collectors.NewsAggregator import NewsAggregator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import Article

sources = [
    "https://www.apnews.com",
    "https://www.npr.org"
]

logging.basicConfig(level = logging.INFO)
def main():
    logging.info("starting scraper.py")

    # connect to the database
    logging.info("try to initialize database")
    init_db()

    news_aggregator = NewsAggregator()

    logging.info("grabbing articles")
    articles = news_aggregator.aggregate_news(sources)

    # run scraping scripts
    logging.info("creating a database session")
    with Session(get_engine()) as session:

        for article in articles:
            session.add(Article(
                title = article.title,
                url = article.url,
                publish_date = article.publish_date,
                source = article.source,
                full_text = article.full_text
            ))
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                logging.warning(f"Duplicate article found: {article.url}")
            except Exception as e:
                session.rollback()
                logging.error(f"Error adding article {article.url} to database: {e}")
        
        logging.info('finished adding articles')
                    

        # websites list npr, bcc, 


if __name__ == "__main__":
    main()

    