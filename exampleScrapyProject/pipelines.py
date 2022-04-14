# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from exampleScrapyProject.settings import MONGODB_CONNECTION_STRING, MONGODB_DATABASE, MONGODB_COLLECTION
import pymongo


# 这个类是scrapy自动生成的一个Pipeline
# 如果这个类名称你不喜欢，可以删掉，写一个自己喜欢的
# class ExamplescrapyprojectPipeline:
#     def process_item(self, item, spider):
#         return item
# 这个类就是我自己创建的
# 变量命名一定要做到名字能反映功能，加强代码可读性
class SaveMovieToMongoPipeline:
    # __init__是python中默认的对象初始化方法，类属性在这里面定义，通常也完成属性的初始化
    def __init__(self):
        # 建立MongoDB的连接代理
        self.client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
        # 利用代理连接特定数据库
        self.db = self.client[MONGODB_DATABASE]

    def process_item(self, item, spider):
        # 利用update_one方法完成数据的去重
        # 该方法的执行逻辑是首先根据filter参数进行查找，如果找到了就更新该数据，如果没找到就根据insert参数来决定是否插入为一个新的记录。
        self.db[MONGODB_COLLECTION].update_one({'name': item['name']}, {'$set': dict(item)}, True)
        return item

    # 爬虫结束时调用，这里用来关闭数据库连接以释放系统资源
    def close_spider(self, spider):
        self.client.close()
