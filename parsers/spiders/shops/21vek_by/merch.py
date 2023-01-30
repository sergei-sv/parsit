import json
from urllib.parse import urljoin

from parsers.core.spiders.base import MerchSpider
from parsers.core.tools.parse import parse_comnum
from parsers.items import MerchItem


class XXIVekBySpider(MerchSpider):
    start_urls = ['https://www.21vek.by/motor_oils/synthetic_5w_40']
    search_url = 'https://search.21vek.by/api/v2.0/search/suggest?q={}'

    def parse(self, response, **kwargs):
        yield from self.parse_item_list(response)

    def parse_item_list(self, response):
        item_list = response.xpath('//ul[@class="b-result"]/li')
        for i in item_list:
            price = i.xpath('.//span/@data-price').get()
            old_price = i.xpath(
                '//span[contains(@class, "result__oldprice")]').get()
            yield MerchItem(
                title=i.xpath('.//span[@class="result__name"]/text()').get(),
                url=i.xpath(
                    './/a[contains(@class, "result__link")]/@href').get(),
                price=price,
                old_price=parse_comnum(old_price),
                discount=int((1 - float(price) / float(
                    old_price)) * 100) if old_price else None
            )

    def parse_search(self, response):
        data = json.loads(response.text)['data'][-1]
        for i in data['items']:
            price = (parse_comnum(i['price']) or '').replace(',', '.')
            if price:
                old_price = (parse_comnum(
                    i['price_without_discount']) or '').replace(',', '.')
                yield MerchItem(
                    title=i['name'],
                    url=urljoin('https://21vek.by', i['url']),
                    price=price,
                    old_price=old_price,
                    discount=int((1 - float(price) / float(
                        old_price)) * 100) if old_price else None
                )
