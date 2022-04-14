# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# item定义了我们所需要爬取的数据的结构
# 这个class是scrapy框架自动生成的，名字不够直观，我们不用这个，在下面自己写一个
class ExamplescrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SsrMovieItem(scrapy.Item):
    # 定义字段非常简单，不需要管这个字段到底是字符串还是数字还是列表
    # 只需要 yourName = scrapy.Field() 就可以了
    name = scrapy.Field()
    tags = scrapy.Field()
    rating = scrapy.Field()
    info = scrapy.Field()
    describe = scrapy.Field()
