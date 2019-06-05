from crawl_commons.spiders.common_spider import *
#精选网站：列表页普通,详情页普通,一小时抓取一次
class SelectedSpider1(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider1" # 定义蜘蛛名

class SelectedSpider2(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider2" # 定义蜘蛛名


class SelectedSpider3(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider3" # 定义蜘蛛名


class SelectedSpider4(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider4" # 定义蜘蛛名


class SelectedSpider5(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider5" # 定义蜘蛛名




#精选网站：列表页js,详情页普通，一小时抓取一次
class SelectedSpiderjs1(CommonSpider):  # 需要继承scrapy.Spider类
    name= "selected_spider_js1" # 定义蜘蛛名

#精选网站：列表页js,详情页js，3小时抓取一次
class SelectedSpiderjs2(CommonSpider):
    name= "selected_spider_js2"


#精选网站：列表页js,详情页js，3小时抓取一次
class SelectedSpiderjs3(CommonSpider):
    name= "selected_spider_js3"


#精选网站：列表页js,详情页js，3小时抓取一次
class SelectedSpiderjs4(CommonSpider):
    name= "selected_spider_js4"


#精选网站：列表页js,详情页js，3小时抓取一次
class SelectedSpiderjs5(CommonSpider):
    name= "selected_spider_js5"