# -*- coding: utf-8 -*-

# Scrapy settings for crawl_selected project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawls'

SPIDER_MODULES = ['crawl_selected.spiders','crawl_auto.spiders']
NEWSPIDER_MODULE = 'crawl_selected.spiders'

#######数据库配置######################################
MONGO_URI = 'mongodb://test:test@10.0.0.157:27017/test_yyh'
MONGO_DB = 'test_yyh'

MONGO_OFFLINE_URI = 'mongodb://test:test@10.0.0.157:27017/test_yyh'
MONGO_OFFLINE_DB = 'test_yyh'

#######种子获取配置#########################################
CRAWL_IP = "10.0.0.36"

CRAWL_INFO_URL = 'http://crawl-db-service:31001/crawlInfo/unique?address=%s&crawlName=%s&project=%s'

CRAWL_INFO_SCHEDULE_URL = 'http://crawl-db-service:31001/crawlInfo?crawlStatus=1&crawlType=ONLINE&address=%s&scheduleType=%s&schedule=%s'



SEED_URL = 'http://crawl-db-service:31001/seed?urlStatus=1&crawlName=%s&ps=100000'

SEED_URL_CRAWLID = 'http://crawl-db-service:31001/seed?urlStatus=1&crawlId=%s&ps=100000'

SEED_STAT_URL = 'http://crawl-operator:31001/seed/stat'

SEED_REGEX_URL = 'http://crawl-db-service:31001/regex?regexName=%s&ps=100000'


########redis配置##################################################
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
REDIS_ITEMS_KEY = '%(spider)s:items'
REDIS_URL = 'redis://root:GemanticYes!@10.0.0.22:7000'
REDIS_START_URLS_KEY = '%(name)s:start_urls'
EXTENSIONS = {
'scrapy.extensions.telnet.TelnetConsole': None,
    'crawl_commons.redis_extension.SetRedisInit': 500
}
#######文件下载请求################
# FILE_DOWNLOAD_URL = 'http://file-download-service:31001/download?urls=%s&publishAt=%s'
FILE_DOWNLOAD_URL = 'http://file-download-service:31001/download'

# Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Default requests serializer is pickle, but it can be changed to any module
# with loads and dumps functions. Note that pickle is not compatible between
# python versions.
# Caveat: In python 3.x, the serializer must return strings keys and support
# bytes as values. Because of this reason the json or msgpack module will not
# work by default. In python 2.x there is no such issue and you can use
# 'json' or 'msgpack' as serializers.
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# Don't cleanup redis queues, allows to pause/resume crawls.
# SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# Alternative queues.
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

# Store scraped item in redis for post-processing.
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }

# The item pipeline serializes and stores the items in this redis key.
#REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
#REDIS_HOST = 'localhost'
#REDIS_PORT = 6379

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
# REDIS_URL = 'redis://root:GemanticYes!@10.0.0.55:7000'

# Custom redis client parameters (i.e.: socket timeout, etc.)
# REDIS_PARAMS  = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True}
# Use custom redis client class.
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# If True, it uses redis' ``SPOP`` operation. You have to use the ``SADD``
# command to add URLs to the redis queue. This could be useful if you
# want to avoid duplicates in your start urls list and the order of
# processing does not matter.
# REDIS_START_URLS_AS_SET = False

# Default start urls key for RedisSpider and RedisCrawlSpider.
#REDIS_START_URLS_KEY = '%(name)s:start_urls'
# SCHEDULER_FLUSH_ON_START = True
# Use other encoding than utf-8 for redis.
# REDIS_ENCODING = 'utf-8'

#########################################################

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_selected (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
FEED_EXPORT_ENCODING = 'utf-8'
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawl_selected.middlewares.CrawlSelectedSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'crawl_commons.middlewares.UserAgentMiddleware':400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'crawl_commons.middlewares.CrawlSelectedDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# EXTENSIONS = {
#     'scrapy_jsonrpc.webservice.WebService': 500,
# }
# JSONRPC_ENABLED = True
# JSONRPC_PORT = [6080, 7030]

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawl_commons.pipelines.CrawlSelectedPipeline': 400,
    # 'scrapy_redis.pipelines.RedisPipeline': 410,
}
#DOWNLOAD_TIMEOUT=30

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# HTTPERROR_ALLOWED_CODES = [304,302,301,404]
# REDIRECT_ENABLED = False
# LOG_FILE='/home/yhye/tmp/scrapy.log'