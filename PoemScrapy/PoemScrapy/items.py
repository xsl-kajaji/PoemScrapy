# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemscrapyItem(scrapy.Item):
    #名句
    sentence = scrapy.Field()
    #来源
    source = scrapy.Field()
    #链接
    href = scrapy.Field()
