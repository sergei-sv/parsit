# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class ParsPipeline:
    def process_item(self, item, spider):
        return item


class CustomImagesPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.images_urls_field, [])
        return [Request(u, meta={'item_title': item['title']}) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'/{request.meta["item_title"]}/{request.url.split("/")[-1]}'
