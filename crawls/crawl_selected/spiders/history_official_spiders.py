from crawl_commons.spiders.common_spider import *

#官方网站：列表页普通,详情页普通,一天二次
class HistoryOfficialSpider1(CommonSpider):  # 需要继承scrapy.Spider类
    name= "history_official_spider1" # 定义蜘蛛名

#官方：列表页js,详情页普通，一天2次
class HistoryOfficialSpiderjs1(CommonSpider):  # 需要继承scrapy.Spider类
    name= "history_official_spider_js1" # 定义蜘蛛名

#官方：列表页js,详情页js，一天2次
class HistoryOfficialSpiderjs2(CommonSpider):  # 需要继承scrapy.Spider类
    name= "history_official_spider_js2" # 定义蜘蛛名
