from urllib.parse import urljoin

from scrapy import Request
from w3lib.url import add_or_replace_parameter

from parsers.core.spiders.base import MerchSpider
from parsers.core.tools.parse import remove_rnt, parse_dotnum
from parsers.items import MerchItem


class OstrovShopByMerchSpider(MerchSpider):
    headers = {
        'cookie': 'PHPSESSID=A42uAeyaumSlUaEX2K9d99FdG6ifUV7R'
    }
    start_urls = [
        ('https://ostrov-shop.by/catalog/bytovaya-khimiya/sredstva-dlya-posudomoechnykh-mashin/somat/'),
    ]
    search_url = 'https://ostrov-shop.by/catalog/?q={}'
    custom_settings = {
        'FEEDS': {
            'spiders/shops/ostrovshop_by/output/merchs.json': {
                'format': 'json', 'overwrite': True}},
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        yield Request(
            self.start_urls[0], self.parse_item_list, headers=self.headers)

    def parse(self, response, **kwargs):
        yield from self.parse_item_list(response)
        max_page = response.xpath(
            '//span[@class="point_sep"]/following-sibling::a/text()').get('0')
        for page in range(2, int(max_page) + 1):
            yield Request(
                url=add_or_replace_parameter(
                    response.url, 'PAGEN_1', str(page)),
                callback=self.parse_item_list
            )

    def parse_item_list(self, response):
        item_list = response.xpath(
            '//div[@class="dinamic_info_wrapper"]')
        for i in item_list:
            yield MerchItem(
                title=remove_rnt(i.xpath('.//a[@title]/span/text()').get()),
                url=urljoin(response.url, i.xpath('.//a[@title]/@href').get()),
                price=parse_dotnum(
                    i.xpath('.//div[@data-currency]/span/span/text()').get()),
                discount=i.xpath(
                    './/div[@class="sale_blocks e"]/div/text()').get('0'),
                old_price=parse_dotnum(
                    i.xpath('.//div[@class="old_price"]/span/text()').get())
            )

    def parse_search(self, response):
        item_list = response.xpath('//div[@class="item_info"]')
        for i in item_list:
            yield MerchItem(
                title=remove_rnt(i.xpath(
                    './div[contains(@class, "title")]/a/span/text()').get()),
                url=urljoin(response.url, i.xpath(
                    './div[contains(@class, "title")]/a/@href').get()),
                price=parse_dotnum(
                    i.xpath('.//div[@data-currency]/span/span/text()').get()),
                discount=i.xpath(
                    './/div[@class="value val"]/text()').get(),
                old_price=parse_dotnum(
                    i.xpath('.//div[@class="old_price"]/span/text()').get())
            )
