from crawl_commons.spiders.common_spider import *
from crawl_commons.spiders.common_redis_spider import *

#单独测试使用
class TestSpider(CommonSpider):  # 需要继承scrapy.Spider类
    name= "test_spider" # 定义蜘蛛名

#单独测试使用
class HistoryTestSpider(CommonSpider):  # 需要继承scrapy.Spider类
    name= "history_test_spider" # 定义蜘蛛名
