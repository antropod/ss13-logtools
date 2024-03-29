from urllib.parse import urljoin
import re
import scrapy
from datetime import date
import logging

# Script for downloading ids of rounds and links to zip files from /tg/ website
# requires scrapy
# to run:
#
# $ scrapy runspider round_archive_urls.py -o data.json

def match_path_pattern(pattern, path):
    r"""
    >>> match_path_pattern(r'/parsed-logs/[a-zA-Z-]+/data/logs/\d{4}/\d{2}/\d{2}/round-\d+\.zip', '/parsed-logs/../')
    False

    >>> match_path_pattern(r'/a/b/c/', '/a/b/')
    True

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/')
    True

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/9123/')
    True

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/9123/01')
    True

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/9123/zz')
    False

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/9123/01/123.zip')
    False

    >>> match_path_pattern(r'/root/\d{4}/\d{2}/', '/root/9123/123.zip')
    False
    """
    pattern_parts = pattern.strip('/').split('/')
    path_parts = path.strip('/').split('/')

    if len(pattern_parts) < len(path_parts):
        return False
    for one_pattern, one_path in zip(pattern_parts, path_parts):
        if not re.match(one_pattern + '$', one_path):
            return False
    return True


class RoundArchiveUrlSpider(scrapy.Spider):
    name = 'round-archive-url'
    allowed_domains = ['tgstation13.org']
    start_urls = ['https://tgstation13.org/parsed-logs/']

    def parse(self, response):
        # get header and parse it
        path_str = response.xpath('//h1/text()').get()[9:]
        assert path_str[0] == path_str[-1] == '/'

        allowed_paths = r'/parsed-logs/[a-zA-Z-]+/data/logs/\d{4}/\d{2}/\d{2}/round-\d+\.zip'

        for path in response.xpath(r'//pre/a/@href').getall():
            next_path = path_str + path
            url = urljoin(response.url, path)
            if match_path_pattern(allowed_paths, next_path):
                if path.endswith('.zip'):  # we are at the end, get the link
                    _, server, _, _, year, month, day = path_str[1:-1].split('/')
                    m = re.match(r"round-(\d+)\.zip", path)
                    if not m:
                        continue
                    round_id = int(m.group(1))
                    yield {
                        'round_id': round_id,
                        'dt': date(int(year), int(month), int(day)),
                        'server': server,
                        'url': urljoin(response.url, url)
                    }
                else:  # Navigate
                    yield scrapy.Request(url=url, callback=self.parse)