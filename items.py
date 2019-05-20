# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_url = scrapy.Field()     # 主页url
    author_uid = scrapy.Field()     # 作者id
    author = scrapy.Field()         # 作者
    fans = scrapy.Field()           # 粉丝数
    concern = scrapy.Field()        # 关注数
    article = scrapy.Field()        # 文章数
    word_count = scrapy.Field()     # 字数
    js_diamond = scrapy.Field()     # 简书钻
    tag = scrapy.Field()            # 个人介绍