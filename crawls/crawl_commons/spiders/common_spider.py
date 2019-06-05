import scrapy
from crawl_commons.spiders.abstract_spider import AbstractSpider

#一级页面抓取通用爬虫，该爬虫不作爬取
class CommonSpider(scrapy.Spider,AbstractSpider):  # 需要继承scrapy.Spider类
    name= "common_spider" # 定义蜘蛛名

    def __init__(self, name=None, **kwargs):
        scrapy.Spider.__init__(self,name=name,kwargs=kwargs)
        AbstractSpider.__init__(self,self.name)

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        return self.do_start_requests()


    def parse(self, response):
        return self.do_parse_list_regex(response)



    def parseDetail(self, response):
        return self.do_parse_detal_regex(response)


    def closed(self,reason):
        self.do_closed(reason)