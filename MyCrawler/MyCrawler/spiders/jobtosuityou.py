# -*- coding: utf-8 -*-
import scrapy
from MyCrawler.items import MycrawlerItem

class JobtosuityouSpider(scrapy.Spider):
    name = "jobtosuityou"
    allowed_domains = ["jobtosuityou.co.uk"]
    start_urls = (
        #'http://www.jobtosuityou.co.uk/',
        'http://www.jobtosuityou.co.uk/directory/Industry/IT_and_Computing',
    )

    def parse(self, response):
        # Get main job body
	main = response.xpath("//td[@class='maincontent']//div")
	# If it exists, get subs
	if len(main)>0:
		subs = main[0].xpath("//div[@align='justify']")
		for entry in subs:
			sitename = entry.xpath("a[@class='sitename']/text()").extract()[0]
			url = entry.xpath("a/@href").extract()[0]
			description = entry.xpath("text()").extract()[1]
			#print sitename, url, description
			item = MycrawlerItem()
			item['title'] = sitename
			item['url'] = url
			item['description'] = description
			yield item
	# Now that we have processed main fields, we get the links
	links = response.xpath("//@href")
	for link in links:
		nextlink = response.urljoin(link.extract())
		r = scrapy.Request(nextlink, self.parse)
		yield r
