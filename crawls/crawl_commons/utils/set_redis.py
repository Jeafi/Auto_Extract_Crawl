import logging
from scrapy.http import Request
from scrapy.utils.request import request_fingerprint


class SetRedis(object):
    server = None
    debug = False
    use_set: bool = False
    logger = logging.getLogger(__name__)
#    '''

    @staticmethod
    def init_set_redis(server, use_set=False, debug=False):
        SetRedis.server = server
        SetRedis.debug = debug
        SetRedis.use_set = use_set

    def __init__(self, server, redis_key, dupefilter_key):
        """
        初始化对象

        :param server: redis client instance
        :type server: redis.client.Redis'

        :param redis_key: RedisSpyder.redis_key
        :type redis_key: string

        :param dupefilter_key: dupefilter.key
        :type dupefilter_key: string
        """
        if not SetRedis.server:
            SetRedis.server = server
        self.redis_key = redis_key
        self.dupefilter_key = dupefilter_key
        if server is None or redis_key is None or dupefilter_key is None:
            raise NameError("server or redis_key or dupefilter_key is None")
    '''
    def __init__(self, spider, dupefilter_key, debug=False):
        if not isinstance(spider, RedisSpider):
            raise TypeError("Expect RedisSpider ")
        self.server = spider.server
        #self.spider_name = spider.name
        self.redis_key = spider.redis_key
        self.dupefilter_key = dupefilter_key
        self.debug = debug
    '''  # '''

    @staticmethod
    def clear_dupe_filter(url, dupefilter_key):
        """
        清除排重顾虑器中url对应的指纹记录
        :param url: url string
        :param dupefilter_key: string
        :type url: string

        return: -1 request创建失败，>=0清除指纹的个数
        """
        req = Request(url)
        if req:
            fingerprint = request_fingerprint(req)
            if SetRedis.debug:
                print(fingerprint, req.url)
            return SetRedis.server.srem(dupefilter_key, fingerprint)
        return -1

    def fill_seeds(self, urls):
        SetRedis.fill_seeds_customlize(urls, self.redis_key, self.dupefilter_key)

    @staticmethod
    def fill_seeds_customlize(urls, redis_key, dupefilter_key):
        """
        填充种子地址到redis，并且清除种子对应的排重记录

        :param urls: url 列表
        :param redis_key: string
        :param dupefilter_key: string
        :type urls: [string]
        """
        push_one = SetRedis.server.sadd if SetRedis.use_set else SetRedis.server.lpush
        for url in urls:
            # clear dupefilter
            SetRedis.clear_dupe_filter(url, dupefilter_key)
            # push new url
            push_one(redis_key, url)

    @staticmethod
    def fill_seed(url, redis_key, dupefilter_key, clear=False):
        """
        设置并清除排重列表对应项,确保url被执行
        :param url:
        :param redis_key:
        :param dupefilter_key:
        :param clear:bool 清除标志
        :return:
        """
        # clear dupefilter
        if clear:
            SetRedis.clear_dupe_filter(url, dupefilter_key)
        SetRedis.fill_url(url, redis_key)

    @staticmethod
    def fill_url(url, redis_key):
        """仅设置,url任务,不处理排重列表
        :param url:
        :param redis_key:
        :return:
        """
        push_one = SetRedis.server.sadd if SetRedis.use_set else SetRedis.server.lpush
        # push new url
        push_one(redis_key, url)
