import scrapy
from scrapy import Selector
from ..items import BaimaItem


class BaiSpiderSpider(scrapy.Spider):
    name = 'baima_spider'
    allowed_domains = ['yuedu.bmsgzw.cn/book/search']
    start_urls = ['https://yuedu.bmsgzw.cn/book/search']

    def parse(self, response):
        for i in range(1,187):
            url = f'https://yuedu.bmsgzw.cn/book/showSearch?json=%7B%22pageNum%22%3A{i}%2C%22type%22%3A%221%22%2C%22' \
                  'key%22%3A%22%22%2C%22roleShow%22%3A%22%22%2C%22tagShow%22%3A%22%22%7D'
            yield scrapy.Request(url=url,callback=self.next,dont_filter=True)


    def next(self,response):
        sel = Selector(response)
        item = BaimaItem()
        lists = sel.xpath('//ul[@id="novelListUl"]/li')

        for li in lists:
            item['book_name'] = li.xpath('./div/h4/a/text()').extract_first()
            item['author'] = li.xpath('./div/p[@class="author"]/a/text()').extract_first().split('：')[1]
            item['click'] = li.xpath('./div/p/span[@class="click"]/span/text()').extract_first()
            item['words'] = li.xpath('./div/p/span[@class="words"]/text()').extract_first().split('：')[1]
            item['ex'] = li.xpath('./div/p/span[@class="ex"]/span/text()').extract_first()
            item['type'] = li.xpath('./div/p/i/text()').extract_first()
            item['status'] = li.xpath('./a/img/@title').extract_first()
            yield item
