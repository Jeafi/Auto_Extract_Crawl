# @Date:   10-Jan-2019
# @Email:  Tang@jeffery.top
# @Filename: test_auto_spider.py
# @Last modified time: 23-Jan-2019



from crawl_commons.spiders.auto_spider import *

#单独测试使用
class TestAutoSpider1(AutoSpider):  # 需要继承scrapy.Spider类
    name= "test_auto_spider1" # 定义蜘蛛名


#单独测试使用
class TestAutoSpider2(AutoSpider):  # 需要继承scrapy.Spider类
    name= "test_auto_spider2" # 定义蜘蛛名


#单独测试使用
class TestAutoSpider3(AutoSpider):  # 需要继承scrapy.Spider类
    name= "test_auto_spider3" # 定义蜘蛛名


#单独测试使用
class HistoryTestAutoSpider1(AutoSpider):  # 需要继承scrapy.Spider类
    name= "history_test_auto_spider1" # 定义蜘蛛名


#单独测试使用
class HistoryTestAutoSpider2(AutoSpider):  # 需要继承scrapy.Spider类
    name= "history_test_auto_spider2" # 定义蜘蛛名


#单独测试使用
class HistoryTestAutoSpider3(AutoSpider):  # 需要继承scrapy.Spider类
    name= "history_test_auto_spider3" # 定义蜘蛛名
