import logging
import datetime
from database.database import init_db, get_engine
from collectors.NewsAggregator import NewsAggregator
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Article

news_sources = [
    "https://www.nytimes.com"
]


def main():
    logging.basicConfig(level = logging.INFO)
    logging.info("starting main.py")

    # connect to the database
    logging.info("try to initialize database")
    init_db()

    # run scraping scripts
    logging.info("creating a database session")
    with Session(get_engine()) as session:
        logging.info("Database connected to successfully")

        # article = Article(
        #     title = "test title",
        #     url = "test url",
        #     source = "test source",
        #     publish_date = datetime.datetime.now(),
        #     full_text = "test text"
        # )
        # session.add(article)
        # session.commit()
        # logging.info("Article added to database")
        stmt = select(Article)
        for row in session.scalars(stmt):
            logging.info(row)

    logging.info("finished main.py")
    news_aggregator = NewsAggregator()
    news_aggregator.aggregate_news(news_sources, max_articles=10)

    for article in news_aggregator.articles:
        logging.info(article)
        logging.info("article added to database")





if __name__ == "__main__":
    main()

    