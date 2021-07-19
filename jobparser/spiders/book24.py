import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=программирование']

    def parse(self,response: HtmlResponse ):
        book_links = response.xpath("//a[@class='product-card__name smartLink']/@href").extract()
        next_page = response.xpath("//lia[@class='pagination__item _link _button _next smartLink']/@href").extract_first()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self,response: HtmlResponse ):
        book_name = response.xpath('//h1/text()').extract_first()
        link = response.url
        book_author = response.xpath('//div[@class="product-characteristic__value"]/a/text()').extract_first()
        book_price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").extract_first()
        book_sale_price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").extract_first()
        book_rating = response.xpath("//span[@class='rating-widget__main-text']/text()").extract_first()

        item = JobparserItem (book_name=book_name,link=link,book_author=book_author, book_price=book_price,book_sale_price=book_sale_price,book_rating=book_rating)
        yield item