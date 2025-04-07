import logging
import datetime
from database.database import init_db, get_engine
from collectors.NewsAggregator import NewsAggregator
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Article

from newspaper import Article
from newspaper import Config

news_sources = [
    "https://www.cnn.com"
]


def main():
    logging.basicConfig(level = logging.INFO)
    logging.info("starting main.py")

    # connect to the database
    logging.info("try to initialize database")
    init_db()

    logging.info("trying some news scraping manually")
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    base_url = 'https://www.wsj.com'
    article = Article(base_url, config=config)

    logging.info("found this article: ", article)


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
        

        logging.info("finished main.py")
        news_aggregator = NewsAggregator()
        news_aggregator.aggregate_news(news_sources, max_articles=10)
        session.add_all(news_aggregator.articles)
        session.commit()

        logging.info("committed all articles to database, printing articles now")
        stmt = select(Article)
        for row in session.scalars(stmt):
            logging.info(row)





if __name__ == "__main__":
    main()

    