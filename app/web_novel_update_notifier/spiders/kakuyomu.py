# -*- coding: utf-8 -*-

import datetime
import scrapy


class KakuyomuSpider(scrapy.Spider):
    name = 'kakuyomu'
    allowed_domains = ['kakuyomu.jp']

    def __init__(self, settings, *args, **kwargs):
        super(KakuyomuSpider, self).__init__(*args, **kwargs)

        self.id = settings.get('KAKUYOMU_ID')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def start_requests(self):
        yield scrapy.Request(f"https://kakuyomu.jp/users/{self.id}/following_works", self.parse)

    def parse(self, response):
        for div in response.xpath('//*[@id="followingWorks-list"]/div/div[2]'):
            print(div.xpath('p/time/@datetime').get())
            title = div.xpath('h4/a/text()').get().strip()
            author = div.xpath('h4/span/a/text()').get().strip()
            novel_id = div.xpath('h4/a/@href').get().strip().split('/')[-1]
            updated_at = datetime.datetime.strptime(div.xpath('p/time/@datetime').get(), '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)
            latest_url = ''

            yield {
                'domain': self.allowed_domains[0],
                'title': title,
                'author': author,
                'novel_id': novel_id,
                'updated_at': updated_at,
                'latest_url': latest_url
            }