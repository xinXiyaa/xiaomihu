# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaimaItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()        # 书本名字
    author = scrapy.Field()           # 作者
    click = scrapy.Field()             # 点击
    words = scrapy.Field()            # 字数
    ex = scrapy.Field()               # 收藏数
    type = scrapy.Field()             # 类型
    status = scrapy.Field()             # 状态

