from urllib.parse import urljoin

from parsers.core.spiders.base import SearchSpider
from parsers.core.tools.parse import remove_rnt
from parsers.items import MerchItem


class OstrovShopBySearchSpider(SearchSpider):
    search_url = 'https://ostrov-shop.by/catalog/?q={}&s=Найти'
    # custom_settings = {
    #     'FEEDS': {
    #         'res_ostrov.json': {'format': 'json'}}, 'FEED_EXPORT_INDENT': 4
    # }

    def parse(self, response, **kwargs):
        for item in response.xpath('//div[@class="dinamic_info_wrapper"]'):
            yield MerchItem(
                title=remove_rnt(item.xpath(
                    './/div[contains(@class, "item-title")]/a/span/text()'
                ).get()),
                url=urljoin(response.url, item.xpath(
                    './/div[contains(@class, "item-title")]/a/@href').get()),
                price=item.xpath('.//div/@data-value').get(),
                discount=item.xpath('.//div[@class="value val"]/text()').get(),
                old_price=item.xpath(
                    './/div[@class="old_price"]/span/text()').get()
            )
