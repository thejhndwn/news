import logging
import datetime
from database.database import init_db, get_engine
from collectors.NewsAggregator import NewsAggregator
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Article

from newspaper import Article, build

sources = [
    "apnews.com",
    "npr.org",
    "bbc.com"
]


def main():
    logging.basicConfig(level = logging.INFO)
    logging.info("starting main.py")

    # connect to the database
    logging.info("try to initialize database")
    init_db()

    news_aggregator = NewsAggregator()


    # run scraping scripts
    logging.info("creating a database session")
    with Session(get_engine()) as session:
        articles = news_aggregator.aggregate_news(sources)
                    

        # websites list npr, bcc, 


if __name__ == "__main__":
    main()

    