# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawl_commons.repository.crawl import *

class CrawlSelectedPipeline(object):
    def __init__(self):
        self.crawldb = CrawlRepository()

    def process_item(self, item, spider):
        self.crawldb.saveCrawlDetail(item)
        if  not spider.name.startswith("history_") and not "test_" in spider.name and not "auto_" in spider.name:
            self.crawldb.updateCrawlStat(item)
        # spider.logger.info("save %s %s" % (item["url"],id))
        return item
