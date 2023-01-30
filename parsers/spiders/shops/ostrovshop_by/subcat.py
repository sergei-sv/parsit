import json
from urllib.parse import urljoin

from scrapy import Request

from parsers.core.spiders.base import SubCatSpider
from parsers.items import SubCatItem


class OstrovShopBySubCatSpider(SubCatSpider):
    custom_settings = {
        'FEEDS': {
            'spiders/shops/ostrovshop_by/output/subcats.json': {
                'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        with open('spiders/shops/ostrovshop_by/output/cats.json') as file:
            cats = json.load(file)
        for cat in cats[:3]:
            yield Request(
                url=cat['url'],
                meta={'cat': cat['name']})

    def parse(self, response, **kwargs):
        subcats = response.xpath('//a[contains(@class, "list__link")]')
        for subcat in subcats:
            yield SubCatItem(
                name=subcat.xpath('./span/text()').get(),
                url=urljoin(response.url, subcat.xpath('./@href').get()),
                cat=response.meta['cat']
            )
