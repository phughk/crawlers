# -*- coding: utf-8 -*-
import scrapy


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = (
        'http://www.dmoz.org/',
    )

    def parse(self, response):
        pass
