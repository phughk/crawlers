# -*- coding: utf-8 -*-
import scrapy
from MyCrawler.items import JobsGoPublicItem

class JobsgopublicSpider(scrapy.Spider):
    name = "jobsgopublic"
    allowed_domains = ["jobsgopublic.com"]
    start_urls = (
        'http://www.jobsgopublic.com/',
    )

    def parse(self, response):
        # get all links
	hrefs = response.xpath("//a/@href").extract()
	for href in hrefs:
		link= response.urljoin(href)
		yield scrapy.Request(link, callback=self.parse)

	# Crawl all jobs
	#head = response.xpath("//div[@class='twenty-one columns']")
	head = response.xpath("//div[@class='twenty-one columns'][ul[@class='vacancy-details']]")
	if len(head)>0:
		# We have the listing header, grab relevant information
		item = JobsGoPublicItem()
		jobTitle = head.xpath("//h1/text()")
		if len(jobTitle)>=1:
			item['title'] = jobTitle[0].extract()
		published= head.xpath("//span[@property='dct:issued']/text()")
		if len(published)>=1:
			item['published'] = published[0].extract()
		arrangement = head.xpath("//span[@property='argot:workingArrangements']/text()")
		if len(arrangement)>=1:
			item['arrangement'] = arrangement[0].extract()
		jobType = head.xpath("//span[@property='argot:jobType']/text()")
		if len(jobType)>=1:
			item['jobType'] = jobType[0].extract()
		salary = head.xpath("//li[strong='Salary:']/text()")
		if len(salary)>=2:
			item['salary'] = salary[1].extract()
		location = head.xpath("//li[string='Location:']/text()")
		if len(location)>=2:
			item['location'] = location[1].extract()
		
		head2 = response.xpath("//div[@id='content']/div[@property='dct:description']")
		fullSummary = head2.extract() # This includes HTML tags
		if len(fullSummary)>=1:
			item['fullSummary'] = fullSummary[0]

		yield item
