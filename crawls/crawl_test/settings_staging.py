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

SPIDER_MODULES = ['crawl_test.spiders']
NEWSPIDER_MODULE = 'crawl_test.spiders'

#######数据库配置######################################
MONGO_URI = 'mongodb://crawl:crawl2get@10.0.0.157:27017/crawl'
MONGO_DB = 'crawl'


MONGO_OFFLINE_URI = 'mongodb://crawl:crawl2get@10.0.0.157:27017/crawl'
MONGO_OFFLINE_DB = 'crawl'

# MYSQL_IP = '10.0.0.20'
# MYSQL_PORT = 3307
# MYSQL_DB = "information"
# MYSQL_USER = "information"
# MYSQL_PASSWORD = "NQM2vhixPFx5"

#######种子获取配置#########################################

CRAWL_INFO_URL = 'http://crawl-db-service:31001/crawlInfo/unique?address=%s&crawlName=%s&project=%s'



SEED_URL = 'http://crawl-db-service:31001/seed?urlStatus=1&crawlName=%s&ps=100000'

SEED_URL_CRAWLID = 'http://crawl-db-service:31001/seed?urlStatus=1&crawlId=%s&ps=100000'

SEED_STAT_URL = 'http://crawl-operator:31001/seed/stat'

SEED_REGEX_URL = 'http://crawl-db-service:31001/regex?regexName=%s&ps=100000'

#######文件下载请求################
FILE_DOWNLOAD_URL = 'http://file-download-service:31001/download'


########redis配置##################################################
#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# The item pipeline serializes and stores the items in this redis key.
#REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
#REDIS_HOST = '10.0.0.55'
#REDIS_PORT = 7000

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
#REDIS_URL = 'redis://dev:GemanticYes!@10.0.0.55:7000'

# Custom redis client parameters (i.e.: socket timeout, etc.)
#REDIS_PARAMS  = {}
# Use custom redis client class.
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# If True, it uses redis' ``SPOP`` operation. You have to use the ``SADD``
# command to add URLs to the redis queue. This could be useful if you
# want to avoid duplicates in your start urls list and the order of
# processing does not matter.
#REDIS_START_URLS_AS_SET = False

# Default start urls key for RedisSpider and RedisCrawlSpider.
#REDIS_START_URLS_KEY = '%(name)s:start_urls'

# Use other encoding than utf-8 for redis.
#REDIS_ENCODING = 'latin1'

#########################################################

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_selected (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'crawl_commons.middlewares.UserAgentMiddleware':400,
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
    'crawl_commons.pipelines.CrawlSelectedPipeline': 300,
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
