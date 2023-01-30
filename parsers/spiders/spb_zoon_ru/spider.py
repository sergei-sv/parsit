import scrapy
from scrapy import Request, Selector
from w3lib.url import url_query_parameter

from parsers.core.spiders.base import BaseSpider
from parsers.core.tools.parse import parse_int, remove_rnt
from parsers.core.tools.main import should_abort_request
from parsers.items import BaseItem


class PolyclinicItem(BaseItem):
    title = scrapy.Field()
    phones = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    social_networks = scrapy.Field()


class SpbZoonRuSpider(BaseSpider):
    custom_settings = {
        # 'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 60000,
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': True},
        'PLAYWRIGHT_ABORT_REQUEST': should_abort_request,
        'FEEDS': {
            '../output_storage/%(name)s/policlinics.json': {'format': 'json'}},
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        yield Request(
            url='https://spb.zoon.ru/medical/type/detskaya_poliklinika/',
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.close_page
            )
        )

    async def parse(self, response, **kwargs):
        page = response.meta['playwright_page']
        total_items = parse_int(response.xpath(
            '//span[contains(@class, "block__count ")]/text()').get())
        for next_items in range(30, int(total_items) + 1, 30):
            await page.wait_for_selector(
                f'(//a[contains(@class, "title-link")])[{next_items}]')
            await page.evaluate(
                'window.scrollBy(0, document.body.scrollHeight)')
        full_html = await page.content()
        await page.close()

        selector = Selector(text=full_html)
        items_urls = selector.xpath(
            '//a[contains(@class, "title-link")]/@href').getall()

        for url in items_urls:
            yield Request(url, self.parse_item)

    def parse_item(self, response):
        item = PolyclinicItem()
        item['title'] = remove_rnt(response.xpath(
            '//div[@class="service-page-header"]//'
            'span[@itemprop="name"]/text()'
        ).get())
        item['phones'] = remove_rnt(response.xpath(
            '//div[@class="service-phones-list"]/span/@data-number').get())
        item['address'] = remove_rnt(''.join(response.xpath(
            '//address[@itemprop="address"]//text()').getall()))
        # item['website'] = remove_url_query(response.xpath(
        #     '//div[@class="service-website-value"]/a/@href').get(''))
        raw_social_networks = response.xpath(
            '//div[contains(@class, "social-list")]/a/@href').getall()
        item['social_networks'] = [
            url_query_parameter(url, 'to') for url in raw_social_networks]
        yield item

    async def close_page(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
