import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/программирование/?stype=0']
#    loc_domain = 'https://www.labirint.ru/'

    def parse(self, response: HtmlResponse):
        books_links = response.xpath ("//div[contains(@class,'card-column')]//a[contains(@class,'product-title-link')]/@href").extract()
        next_page = response.xpath ("//a[@class='pagination-next__text']/@href").extract_first()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_name = response.xpath ('//h1/text()').extract_first()
        link = response.url
        book_author = response.xpath ('//div[@class="authors"]/a/text()').extract()
        book_price = response.xpath ("//span[@class='buying-priceold-val-number']/text()").extract_first()
        book_sale_price = response.xpath ("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        book_rating = response.xpath ("//div[@id='rate']/text()").extract_first()

        item = JobparserItem (book_name=book_name,link=link,book_author=book_author, book_price=book_price, book_sale_price=book_sale_price, book_rating=book_rating)
        yield item

