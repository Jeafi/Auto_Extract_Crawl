# @Date:   10-Jan-2019
# @Email:  Tang@jeffery.top
# @Filename: test_auto_spider.py
# @Last modified time: 23-Jan-2019



from crawl_commons.spiders.auto_spider import *
from crawl_commons.spiders.common_spider import *
#单独测试使用
class TestAutoErrorSpider(AutoSpider):  # 需要继承scrapy.Spider类
    name= "test_auto_error_spider" # 定义蜘蛛名

#单独测试使用
class HistoryTestAutoErrorSpider(AutoSpider):  # 需要继承scrapy.Spider类
    name= "history_test_auto_error_spider" # 定义蜘蛛名



#单独测试使用
class TestErrorSpider(CommonSpider):  # 需要继承scrapy.Spider类
    name= "test_error_spider" # 定义蜘蛛名



#单独测试使用
class HistoryTestAutoSpider(CommonSpider):  # 需要继承scrapy.Spider类
    name= "history_test_error_spider" # 定义蜘蛛名
