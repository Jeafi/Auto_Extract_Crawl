# encoding=utf-8
from crawl_commons.utils.article_util import *
from crawl_commons.utils.string_util import *
from html_similarity import style_similarity
from html_similarity import structural_similarity
from crawl_commons.repository.crawl import *
from crawl_commons.utils.annotation import *
import logging


class TemplateComparator(object):

    def __init__(self,crawlDB,style_weight=0.8):
        """获取数据库及表名
        :param style_weight: 比较结果风格权重，一般>=0.7
        """
        self.logger = logging.getLogger("templateComparator")
        self.STYLE_WEIGHT = style_weight
        self.crawlDB = crawlDB

    @staticmethod
    def compare(html1, html2):
        if html1 == html2:
            return 1,1
        # print("html1",html1)
        # print("html2",html2)
        style_rate = style_similarity(html1, html2)
        struc_rate = structural_similarity(html1, html2)
        return style_rate, struc_rate

    def get_similarity(self, style_rate, struc_rate):
        """综合相似度，基于STYLE_WEIGHT
        :param style_rate:
        :param struc_rate:
        :return:
        """
        similarity = self.STYLE_WEIGHT*style_rate+(1-self.STYLE_WEIGHT)*struc_rate
        # if TemplateComparator.debug:
        # print(style_rate, struc_rate, similarity)
        return similarity



    def compare_baseline(self, base, page):
        if base['time'] >= page['time']:
            return
        style_rate, struc_rate = TemplateComparator.compare(base['html'], page['html'])
        similarity = self.get_similarity(style_rate, struc_rate)
        id = ArticleUtils.getArticleId(page['_id'] + "_" + base['time'] + "_" + page['time'])

        compare = {"_id":id,"seed": page['seed'], "depthNumber": page['depthNumber'], "parse": page["parse"],
                   "last_time": base['time'], "current_time": page['time'], "style_rate": style_rate,
                   "struc_rate": struc_rate, "similarity": similarity, "last_count": page['all'],
                   "success_count": page['success'],"crawlId":page['crawlId'],"crawlName":page['crawlName']}
        self.crawlDB.save_compare_result(compare)
        self.crawlDB.save_baseline(page)
        # print('callback ',self.callback, not self.callback)
        # if self.callback:  # != None:
        #     self.callback.callback(compare)

    @staticmethod
    def get_row(result):
        # print(type(result))
        try:
            page = result.next()
        except StopIteration:
            return None, False
        return page, True

    def run(self,parse="detail",depthNumber=0,crawlId=22):
        crawlStats = self.crawlDB.get_crawl_stat(crawlId,parse,depthNumber)
        if crawlStats is None:
            return
        crawlStat,hasNext = self.get_row(crawlStats)
        while hasNext:
            if StringUtils.isEmpty(crawlStat["html"]):
                crawlStat,hasNext = self.get_row(crawlStats)
                continue
            baseline = self.crawlDB.get_baseline(crawlStat["_id"])
            if baseline is None:
                self.crawlDB.save_baseline(crawlStat)
                crawlStat, hasNext = self.get_row(crawlStats)
                continue
            self.compare_baseline(baseline,crawlStat)
            crawlStat, hasNext = self.get_row(crawlStats)


    def run_task(self,crawlId):
        self.logger.info("monitor start run list 0 crawlId="+str(crawlId))
        self.run("list",0,crawlId)
        self.logger.info("monitor start run detail 0 crawlId=" + str(crawlId))
        self.run("detail", 0, crawlId)
        self.logger.info("monitor start run list 1 crawlId=" + str(crawlId))
        self.run("list",1,crawlId)
        self.logger.info("monitor start run list 2 crawlId=" + str(crawlId))
        self.run("list",2,crawlId)
        self.logger.info("monitor start run list 3 crawlId=" + str(crawlId))
        self.run("list",3, crawlId)
        self.logger.info("monitor end " + str(crawlId))
