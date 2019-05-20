# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import os
import csv
from pymongo import MongoClient

# class JianshuPipeline(object):
#     def __init__(self):
#         self.wb = Workbook()
#         self.ws = self.wb.active
#         self.ws.append(['作者', '关注', '粉丝', '文章', '字数', '简书钻', '个人介绍', '作者id', '主页url'])
#
#     def process_item(self, item, spider):
#         line = [item['author'], item['concern'], item['fans'], item['article'], item['word_count'], item['js_diamond'], item['tag'], item['author_uid'], item['author_url']]
#         self.ws.append(line)
#         self.wb.save('jianshu.xlsx')
#         return item
#
#     # def __init__(self):
    #     store_file = os.path.dirname(__file__)+'/spiders/jianshu.csv'
    #     headers = ['作者', '关注', '粉丝', '文章', '字数', '简书钻', '个人介绍', '作者id', '主页url']
    #     self.file = open(store_file, 'w', encoding='utf-8')
    #     self.writer = csv.DictWriter(self.file, headers)
    #     self.writer.writeheader()
    #
    # def process_item(self, item, spider):
    #     line = [item['author'], item['concern'], item['fans'], item['article'], item['word_count'], item['js_diamond'], item['tag'], item['author_uid'], item['author_url']]
    #     self.writer.writerows(line)
    #     #self.writer.writerows(line)
    #     return item
    #
    # def close_spider(self,spider):
    #     self.file.close()

MongoDBname = 'jianshu'     #  数据库名
MongoItem = 'num'         #  数据库集合名

class JianshuPipeline(object):
    def __init__(self):
        dbName = MongoDBname             # 给数据库添加名字
        client = MongoClient()           # 创建连接对象client
        db = client[dbName]              # 使用的数据库
        self.post = db[MongoItem]

    def process_item(self, item, spider):
        item = dict(item)
        self.post.insert(item)
        return item