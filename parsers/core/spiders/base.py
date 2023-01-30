import re
from urllib.parse import quote_plus

import scrapy
from scrapy import Request

from parsers.core.spiders import SpiderNameMixin


class MetaSpider(type):
    def __init__(cls, cls_name, superclasses_tuple, attributes_dict):
        super().__init__(cls_name, superclasses_tuple, attributes_dict)
        if cls.suffix:
            cls.name = '_'.join((cls.get_spidername(), cls.suffix))
        else:
            cls.name = cls.get_spidername()

    def get_cls_name(cls) -> str:
        """
        Get class name as part of module path.

        :return: from 'parsers.spiders.shop.mila_by.spider' get 'shop.mila_by'
        """
        return '.'.join(cls.__module__.split('.')[2:-1])


class BaseSpider(SpiderNameMixin, scrapy.Spider, metaclass=MetaSpider):
    suffix = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        pass


class CatSpider(BaseSpider):
    """
    Class for parsing categories of merchandises.
    """
    suffix = 'cat'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubCatSpider(BaseSpider):
    """
    Class for parsing subcategories of merchandises.
    """
    suffix = 'subcat'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MerchSpider(BaseSpider):
    """
    Class for parsing merchandises.
    """
    suffix = 'merch'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SearchSpider(BaseSpider):
    """
    Class for parsing search query.
    """
    suffix = 'search'
    search_url = NotImplemented
    search = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.search:
            self.start_urls = [self.search_url.format(quote_plus(self.search))]
