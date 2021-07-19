# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    book_name = scrapy.Field()
    link = scrapy.Field ()
    book_author = scrapy.Field ()
    book_price = scrapy.Field ()
    book_sale_price = scrapy.Field ()
    book_rating = scrapy.Field ()
    pass