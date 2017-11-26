# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from medium.items import MediumItem

class NewsSpider(CrawlSpider):
    name = "news"
    allowed_domains = ["www.olx.com.pk"]
    start_urls = [
        'https://www.olx.com.pk/computers-accessories/','https://www.olx.com.pk/games-entertainment/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
             callback="parse_item",
             follow=True),)
    
    def parse_item(self, response):
        item_links = response.css('.large > .detailsLink::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)



    def parse_detail_page(self, response):
        title = response.css('h1::text').extract()[0].strip()
        item = MediumItem()
        item['title'] = title
        item['url'] = response.url
        yield item