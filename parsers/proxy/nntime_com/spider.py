import re
import scrapy

from parsers.items import BaseItem


class ProxyItem(BaseItem):
    proxy = scrapy.Field()


class ProxiesSpider(scrapy.Spider):
    name = 'proxy:nntime_com'
    start_urls = ['http://www.nntime.com/proxy-list-01.htm']
    # custom_settings = {
    #     'FEEDS': {
    #         'proxy/proxy.json': {'format': 'json'}
    #     }
    # }

    def parse(self, response, **kwargs):
        pattern = r':\"([\+\w]+)\)'
        script_text = response.xpath('//head//script/text()').get()
        keys_dict = {k: v for k, v in re.findall(r'(\w)=(\d)', script_text)}

        proxies = []
        for row in response.xpath('//*[@id="proxylist"]/tr'):
            port_expression = row.xpath('./td/script/text()').get()
            keys_str = re.findall(pattern, port_expression)[0]
            port = ''.join([keys_dict.get(k) for k in keys_str if k != '+'])
            proxy = f'{row.xpath("./td[script]/text()").get()}:{port}'
            proxies.append(proxy)

        with open('proxy/proxy.txt', 'w') as file:
            for i in proxies:
                file.write(f'{i}\n')
