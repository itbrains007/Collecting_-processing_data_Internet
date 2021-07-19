import re
import pymongo

class JobparserPipeline:

    def __init__(self):
        MONGO_HOST = "localhost"
        MONGO_PORT = 27017
        MONGO_DB = "mydb"
        MONGO_COLLECTION = "books"

        self.client = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db.MONGO_COLLECTION

    def process_item(self, item, spider):
        item = dict(item)
        item['book_name'] = re.sub("^\s+|\s+$", "", item['book_name'])
        if spider.name in 'book24':
            item['book_author'] = re.sub("^\s+|\s+$", "", item['book_author'])

        if spider.name in 'labirint':
            for i in range(len(item['book_author'])):
                item['book_author'][i] = str(re.sub("^\s+|\s+$","",item['book_author'][i]))

        if item['book_price']:
            item['book_price'] = re.sub("^\s+|\s+$","",item['book_price'])
            item['book_price'] = float(item['book_price'].replace ("₽","").replace (",",""))

        if item['book_sale_price']:
            item['book_sale_price'] = re.sub ("^\s+|\s+$","",item['book_sale_price'])
            item['book_sale_price'] = float(item['book_sale_price'].replace ("₽","").replace (",",""))

        if item['book_rating']:
            item['book_rating'] = re.sub ("^\s+|\s+$","",item['book_rating'])

        self.db.inventory.insert_one(dict(item))
        return item
