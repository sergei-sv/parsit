from urllib.parse import urljoin

from parsers.core.spiders.base import CatSpider
from parsers.items import CatItem


class OstrovShopByCatSpider(CatSpider):
    start_urls = ['https://ostrov-shop.by/catalog/']
    custom_settings = {
        'FEEDS': {
            'spiders/shops/ostrovshop_by/output/cats.json': {
                'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response, **kwargs):
        cats = response.xpath('//div[contains(@class, "item-catalog")]')
        for cat in cats:
            yield CatItem(
                name=cat.xpath('.//a/span/text()').get(),
                url=urljoin(response.url, cat.xpath('.//a/@href').get())
            )
