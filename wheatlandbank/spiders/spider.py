import scrapy

from scrapy.loader import ItemLoader

from ..items import WheatlandbankItem
from itemloaders.processors import TakeFirst


class WheatlandbankSpider(scrapy.Spider):
	name = 'wheatlandbank'
	start_urls = ['https://wheatland.bank/news/']

	def parse(self, response):
		post_links = response.xpath('//*[@class="read-moew hidden-xs"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="paginationLink"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h3/text()').get()
		description = response.xpath('//div[@class="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[contains(@class,"article-date")]/text()').get()

		item = ItemLoader(item=WheatlandbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
