import logging
from scrapy import signals
from crawl_commons.utils.set_redis import SetRedis

logger = logging.getLogger(__name__)


class SetRedisInit(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.item_count = 11
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls(crawler)
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        # crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        # return the extension object
        return ext

    def spider_opened(self, spider):
        """启动spider时初始化SetRedis,和spider
        开始任务, push start urls into redis
        :param spider:
        :return:
        """
        if not SetRedis.server:
            spider.init_set_redis()
        if not spider.df_key:
            spider.init_df_key()
        spider.start_tasks()
