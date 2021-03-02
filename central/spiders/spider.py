import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CentralItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class CentralSpider(scrapy.Spider):
	name = 'central'
	start_urls = ['https://www.centralbank.cy/el/announcements']

	def parse(self, response):
		post_links = response.xpath('//article[@class="text-center"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//div[@class="text-center"]/text()').get().strip().split(', ')[1]
		title = response.xpath('//h1[@class="text-center"]/text()').get()
		content = response.xpath('//div[@class="row"]/div[@class="col-xs-12 col-sm-12 col-md-12 col-lg-12"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=CentralItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
