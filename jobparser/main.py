from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.book24 import Book24Spider
from jobparser.spiders.labirint import LabirintSpider

if __name__ == '__main__':
    crawler_settins = Settings()
    crawler_settins.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settins)
    process.crawl(Book24Spider)
    process.crawl(LabirintSpider)

    process.start()