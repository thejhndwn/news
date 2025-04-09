import logging
import datetime
from database.database import init_db, get_engine
from collectors.NewsAggregator import NewsAggregator
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Article

from newspaper import Article, build


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
        

        #url = "https://www.npr.org/2025/04/08/nx-s1-5355624/world-markets-international-trump-tariffs"
        url = "https://www.bbc.com/news/live/cp8vyy35g3mt"

        cnn_paper = build("https://cnn.com", memoize_articles=False)
        logging.info(len(cnn_paper.articles)) 

        # websites list npr, bcc, 


if __name__ == "__main__":
    main()

    