from .NewsAggregationStrategy import NewsAggregationStrategy
from ..NewsArticle import NewsArticle
from typing import List
import logging
import datetime
import newspaper

from newspaper import Article
from newspaper import Config

class NewspaperAggregationStrategy():
    def __init__(self, 
                 sources = [
                    "https://www.apnews.com",
                    "https://www.npr.org"
                    ]):
        print("running up NewspaperAggregationStrategy")
        self.sources = sources
        self.articles = self.get_articles_from_source(sources)
        


    def get_articles_from_source(self, sources = []) -> List[Article]:
        articles = []
        for source_url in sources:
            try:
                source = newspaper.build(source_url, memoize_articles = False)
                articles.extend(source.articles)
            except Exception as e:
                logging.error(f"Error grabbing article from {source_url}")
        return articles

    def get_articles(self, num = 10):
        if len(self.articles) < num:
            self.articles.extend(self.get_articles_from_source(self.sources))

        articles = []
        for a in self.articles[:num]:
            a.download()
            a.parse()
            news_article = NewsArticle(
                    title = a.title,
                    url = a.url,
                    publish_date = str(a.publish_date) or str(datetime.datetime.now()),
                    full_text = a.text)

            articles.append(news_article)
        del self.articles[:num]
        return articles

    def get_article_from_url(self, url:str):
        article = Article(url)
        article.download()
        article.parse()
        news_article = NewsArticle(
                title = article.title,
                url = article.url,
                publish_date = str(article.publish_date) or str(datetime.datetime.now()),
                full_text = article.text)
        return news_article

