import json
from math import ceil
from urllib.parse import urljoin

import scrapy
from scrapy import Request

from parsers.core.spiders.base import BaseSpider
from parsers.items import BaseItem


class LandingItem(BaseItem):
    title = scrapy.Field()
    obid = scrapy.Field()
    website = scrapy.Field()
    image_list = scrapy.Field()
    image_urls = scrapy.Field()


class LandingfolioComSpider(BaseSpider):
    items_url = (
        'https://www.landingfolio.com/api/inspiration?page={}'
        '&sortBy=free-first')
    start_urls = [
        'https://www.landingfolio.com/api/category/parent/inspiration']
    custom_settings = {
        'FEEDS': {
            '../output_storage/%(name)s/landings.json': {'format': 'json'}},
        'FEED_EXPORT_INDENT': 4,
        # if you need save images - set IMAGES_STORE
        # 'IMAGES_STORE': '../output_storage/landingfolio_com/images/',
    }

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        count = 0
        for i in data:
            count += i['count']
        max_page = ceil(count/80)
        for page in range(max_page + 1):
            yield Request(
                url=self.items_url.format(page),
                callback=self.parse_item
            )

    def parse_item(self, response):
        data = json.loads(response.text)
        for item in data:
            img_list = list()
            img_urls = list()
            for i in item['screenshots']:
                screenshots = dict()
                screenshots['title'] = i['title']
                desktop_image = urljoin(
                    'https://landingfoliocom.imgix.net',
                    i['images']['desktop'])
                screenshots['desktop'] = desktop_image
                screenshots['mobile'] = urljoin(
                    'https://landingfoliocom.imgix.net',
                    i['images']['mobile'])
                img_list.append(screenshots)
                img_urls.append(desktop_image)
            landing = LandingItem(
                title=item['title'],
                obid=item['_id'],
                website=item['url'],
                image_list=img_list,
                image_urls=img_urls,
            )
            yield landing
