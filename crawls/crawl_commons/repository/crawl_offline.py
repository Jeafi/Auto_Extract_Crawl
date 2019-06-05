# @Date:   11-Jan-2019
# @Email:  Tang@jeffery.top
# @Filename: crawl.py
# @Last modified time: 18-Jan-2019



import pymongo
from scrapy.utils.project import get_project_settings
from crawl_commons.utils.time_util import *
from crawl_commons.utils.annotation import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.string_util import *
from crawl_commons.repository.filedownload import *

import logging

@singleton
class CrawlOfflineRepository:

    def __init__(self):
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_OFFLINE_URI'))
        self.db = self.client[settings.get('MONGO_OFFLINE_DB')]
        self.logger = logging.getLogger("crawlOfflineRepository")
        self.crawlHtml = self.db.get_collection("crawlHtml")

    def saveCrawlHtml(self,detail):
        if not ArticleUtils.isFile(detail["url"]):
            now = TimeUtils.getNowMill()
            html = {"_id":detail["_id"]}
            html["content"] = detail["html"]
            html["url"] = detail["url"]
            html["publishAt"] = detail["publishAt"]
            html["title"] = detail["title"]
            html["referer"] = detail["referer"]
            html["crawlId"] = detail["crawlId"]
            html["updateAt"] = now
            self.crawlHtml.save(html)

