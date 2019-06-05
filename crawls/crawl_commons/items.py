# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlResultItem(scrapy.Item):
    referer = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    mediaFrom = scrapy.Field()
    category = scrapy.Field()
    urlLabel = scrapy.Field()
    crawlName = scrapy.Field()
    crawlId = scrapy.Field()
    title = scrapy.Field()
    headTitle = scrapy.Field()
    author = scrapy.Field()
    year = scrapy.Field()
    timeRange = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    publishAt = scrapy.Field()
    authorInfo = scrapy.Field()
    contentSource = scrapy.Field()
    organization = scrapy.Field()
    contentCreatAt = scrapy.Field()
    contentNumber = scrapy.Field()
    contentEffectiveAt = scrapy.Field()
    contentEffect = scrapy.Field()
    contentImages = scrapy.Field()
    contentFiles = scrapy.Field()
    contentSnapshot = scrapy.Field()
    timestamp = scrapy.Field()
    parse = scrapy.Field()
    html = scrapy.Field()
