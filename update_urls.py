from scrapy.crawler import CrawlerProcess
from spiders.round_archive_urls import RoundArchiveUrlSpider
from sqlalchemy.orm import sessionmaker
from common import create_default_engine

from logtools.models.round_archive_url import RoundArchiveUrl


class StoreIntoDatabase:

    def __init__(self, engine):
        self.engine = engine

    @classmethod
    def from_crawler(cls, crawler):
        engine = create_default_engine()
        RoundArchiveUrl.metadata.create_all(engine)
        return cls(engine=engine)

    def open_spider(self, spider):
        engine = self.engine
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        try:
            self.session.commit()
        finally:
            self.session.close()

    def process_item(self, item, spider):
        obj = RoundArchiveUrl(**item)
        self.session.merge(obj)
        return item


def main():
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            StoreIntoDatabase: 500
        }
    })
    process.crawl(RoundArchiveUrlSpider)
    process.start()


if __name__ == "__main__":
    main()