import scrapy


class BaseItem(scrapy.Item):
    url = scrapy.Field()


class CatItem(BaseItem):
    pass


class SubCatItem(BaseItem):
    cat = scrapy.Field()


class MerchItem(BaseItem):
    title = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()  # % discount
    old_price = scrapy.Field()
