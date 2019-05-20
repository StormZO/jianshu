# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem
from scrapy_redis.spiders import RedisSpider


class JsSpider(RedisSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    redis_key = 'jianshu_start'
    #start_urls = ['https://www.jianshu.com/u/326092249758']
    user_url = 'https://www.jianshu.com{}'                              # 主页url
    fans_url = 'https://www.jianshu.com/users/{}/followers?page={}'     # 粉丝页url
    concern_url = 'https://www.jianshu.com/users/{}/following?page={}'  # 关注页url
    # def start_requests(self):
    #     yield scrapy.Request(url=self.user_url.format(self.uid), callback=self.parse)

    def parse(self, response):
        item = JianshuItem()
        item['author_uid'] = response.xpath("//a[@class='name']/@href").get()
        item['author_url'] = response.url
        item['author'] = response.xpath("//a[@class='name']/text()").get()
        item['fans'] = response.xpath("//div[@class='info']/ul/li[2]//p/text()").get()
        item['concern'] = response.xpath("//div[@class='info']/ul/li[1]//p/text()").get()
        item['article'] = response.xpath("//div[@class='info']/ul/li[3]//p/text()").get()
        item['word_count'] = response.xpath("//div[@class='info']/ul/li[4]//p/text()").get()
        item['js_diamond'] = response.xpath("//div[@class='info']/ul/li[6]//p/text()").extract_first()
        item['tag'] = response.xpath("//div[@class='js-intro']/text()").extract_first()
        #print(item)
        yield item
        uid = item['author_url'].split('/')[-1]
        page = 1
        yield scrapy.Request(url=self.fans_url.format(uid,page), callback=self.parse_fans, meta={'page': page})
        yield scrapy.Request(url=self.concern_url.format(uid,page), callback=self.parse_concern, meta={'page': page})

    def parse_concern(self, response):
        page = int(response.meta['page'])+1
        user_list = response.xpath("//ul[@class='user-list']/li")
        for user in user_list:
            uid = user.xpath("./a[@class='avatar']/@href").get()
            yield scrapy.Request(url=self.user_url.format(uid), callback=self.parse)
        id = response.url.split('/')[-2]
        if len(user_list)+1 > 9:
            yield scrapy.Request(url=self.concern_url.format(id, page), callback=self.parse_concern,meta={'page': page})


    def parse_fans(self,response):
        page = int(response.meta['page']) + 1
        user_list = response.xpath("//ul[@class='user-list']/li")
        for user in user_list:
            uid = user.xpath("./a[@class='avatar']/@href").get()
            yield scrapy.Request(url=self.user_url.format(uid), callback=self.parse)
        id = response.url.split('/')[-2]
        if len(user_list) + 1 > 9:
            yield scrapy.Request(url=self.fans_url.format(id, page), callback=self.parse_fans,
                                 meta={'page': page})

