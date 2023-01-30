import re
import subprocess
from urllib.parse import quote_plus


search = 'pampers 6-10 кг'
spiders_list = [
    'shops.ostrovshop_by_search',
]


def start_search(search_text: str, spiders: list):
    search_phrase = re.search(r'[Нн]айти (.*)', search_text).group(1)
    for spider in spiders:
        raw_cmd = (
            'scrapy crawl {spider} -a search={search} -O merchs.csv')
        cmd = raw_cmd.format(spider=spider, search=search_phrase)
        subprocess.run(cmd.split())


if __name__ == '__main__':
    start_search(search, spiders_list)
