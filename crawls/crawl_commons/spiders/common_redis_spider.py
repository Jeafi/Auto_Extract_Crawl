import scrapy
from crawl_commons.items import CrawlResultItem

from crawl_commons.repository.seed import *
from scrapy_redis.spiders import RedisSpider
from crawl_commons.repository.crawl import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.string_util import *
from crawl_commons.utils.set_redis import *
import pickle
import scrapy_redis.defaults as srd
from crawl_commons.utils.set_redis import SetRedis
from crawl_commons.spiders.abstract_spider import AbstractSpider
import json
#一级页面抓取通用爬虫，该爬虫不作爬取
class CommonRedisSpider(RedisSpider,AbstractSpider):  # 需要继承scrapy.Spider类
    name= "common_redis_spider" # 定义蜘蛛名
    _dupefilter_template = None  # df_key模板, from settings,静态即可
    # crawlId = 0
    def __init__(self, name=None, **kwargs):
        # super(CommonRedisSpider,self).__init__(name=name,kwargs=kwargs)
        # self.seedDB = SeedRepository()
        # self.crawlDB = CrawlRepository()
        RedisSpider.__init__(self, name=name, kwargs=kwargs)
        AbstractSpider.__init__(self, self.name)
        self.df_key = None  # dupefilter key

    def init_set_redis(self):
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', srd.START_URLS_AS_SET)
        SetRedis.init_set_redis(self.server, use_set)

    def init_df_key(self):
        if not CommonRedisSpider._dupefilter_template:
            # 如果在__init__中初始化self.crawler.engine.slot.scheduler尚不存在
            try:
                CommonRedisSpider._dupefilter_template = self.crawler.engine.slot.scheduler.dupefilter_key
            except AttributeError:
                CommonRedisSpider._dupefilter_template = self.settings.get("SCHEDULER_DUPEFILTER_KEY",
                                                                      srd.defaults.SCHEDULER_DUPEFILTER_KEY)
        self.df_key = CommonRedisSpider._dupefilter_template % {'spider': self.name}

    def get_metakey(self, url):
        return self.redis_key + "+" + url

    def _set_redis_key(self, url, meta, clear=False):
        """url存入start_url,同时
        序列化meta data至redis, key: metakey
        :param url:
        :param meta:
        :param clear: bool清除dupefileter标志
        :return:
        """
        metas = pickle.dumps(meta)
        self.server.set(self.get_metakey(url), metas)
        SetRedis.fill_seed(url, self.redis_key, self.df_key, clear=clear)

    def start_tasks(self):  # 由此方法通过下面链接爬取页面, 原start_requests()
        self.do_start_requests()


    def do_request(self,url, meta,dont_filter=False,cleanup=False):
        self._set_redis_key(url, meta,cleanup)


    def _get_meta_by_url(self, url):
        urlkey = self.get_metakey(url)
        metas = self.server.get(urlkey)
        if metas:
            meta = pickle.loads(metas)
            self.server.delete(urlkey)
            return meta
        else:
            self.logger.info("%s not found in redis_key" % url)

    def make_requests_from_url(self, url):
        meta = self._get_meta_by_url(url)
        parse = self.parse
        try:
            if meta is not None and "parse" in meta and meta["parse"] is not None and meta["parse"] == "detail":
                parse = self.parseDetail
        except KeyError:
            pass
        return scrapy.Request(url=url, meta=meta, callback=parse)

    def parse(self, response):
        self.do_parse_list_regex(response)



    def parseDetail(self, response):
        return self.do_parse_detal_regex(response)



    def closed(self,reason):
        self.do_closed(reason)