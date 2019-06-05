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
from crawl_commons.repository.crawl_offline import *



import logging


class CrawlRepository:

    def __init__(self):
        settings = get_project_settings()

        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client[settings.get('MONGO_DB')]
        self.logger = logging.getLogger("crawlRepository")
        self.downloadDB = FileDownloadRepository()
        self.offlineDB = CrawlOfflineRepository()
        self.crawlDetail = self.db.get_collection("crawlDetail")
        self.crawl = self.db.get_collection("crawl")
        self.crawlSnapshot = self.db.get_collection("crawlSnapshot")
        self.crawlDetailTest = self.db.get_collection("crawlDetailTest")
        self.crawlSnapshotTest = self.db.get_collection("crawlSnapshotTest")
        self.crawlTest = self.db.get_collection("crawlTest")
        self.crawlStat = self.db.get_collection("crawlStat")
        self.baseline = self.db.get_collection("baseline")
        self.comparison = self.db.get_collection("comparisonResult")

        # self.downloadFiles = "downloadFiles"

    def saveCrawlDetail(self,item):
        now = TimeUtils.getNowMill()
        detail = dict(item)
        id = ArticleUtils.getArticleId(detail["url"])
        detail["_id"] = id;
        detail["createAt"] = now
        detail["updateAt"] = now
        isErrorPage = ArticleUtils.isErrorPage(detail)
        if isErrorPage:
            self.logger.info("errorPage %s %s" % (detail["url"], id))
            return

        detail.pop("parse")
        crawlName = detail["crawlName"]
        if "headTitle" in detail:
            detail.pop("headTitle")
        if "timestamp" in detail:
            detail.pop("timestamp")
        isFile = ArticleUtils.isFile(detail["url"])
        isTest = not ArticleUtils.isNotTest(crawlName)
        if "html" in detail:
            if not isTest and not isFile:
                self.offlineDB.saveCrawlHtml(detail)
            detail.pop("html")
        if isFile:
            detail["fileType"] = "file"
            if isTest:
                self.crawlDetailTest.save(detail)
                self.crawlTest.save(detail)
            else:
                self.crawlDetail.save(detail)
                self.crawl.save(detail)
            if "publishAt" in detail:
                self.downloadDB.download([detail["url"]], str(detail["publishAt"]))
            # files = ArticleUtils.getDownloadFile([detail["url"]],detail["publishAt"])
            # for file in files:
            #     self.db[self.downloadFiles].save(file)
            self.logger.info("save file %s %s" % (item["url"], id))
        elif "content" in detail and StringUtils.isNotEmpty(detail["content"]):
            if "contentSnapshot" in detail:
                snapshotDetail = {"_id":id,"content":detail["contentSnapshot"],"url":detail["url"],"updateAt":now}
                if isTest:
                    self.crawlSnapshotTest.save(snapshotDetail)
                else:
                    self.crawlSnapshot.save(snapshotDetail)

                detail.pop("contentSnapshot")
            if isTest:
                self.crawlDetailTest.save(detail)
            else:
                self.crawlDetail.save(detail)

            self.logger.info("save %s %s" % (item["url"], id))
            urls = []
            if "contentImages" in detail:
                contentImages = json.loads(detail["contentImages"])
                for img in contentImages:
                    urls.append(img["url"])
                detail.pop("contentImages")
            if "contentFiles" in detail:
                contentFiles = json.loads(detail["contentFiles"])
                for fileUrl in contentFiles:
                    urls.append(fileUrl["url"])
                detail.pop("contentFiles")
            if len(urls) > 0 and "publishAt" in detail:
                self.downloadDB.download(urls,str(detail["publishAt"]))
            detail.pop("content")
            if isTest:
                self.crawlTest.save(detail)
            else:
                self.crawl.save(detail)
            # files = ArticleUtils.getDownloadFile(urls,detail["publishAt"])
            # for file in files:
            #     self.db[self.downloadFiles].save(file)
        else :
            self.logger.info("no content %s" % (item["url"]))


    def saveFileCrawlDetail(self,meta,url):
        item = ArticleUtils.meta2item(meta,url)
        self.saveCrawlDetail(item)

    def updateCrawlStat(self, item):
        if "content" not in item:
            return
        url = item["url"]
        if ArticleUtils.isFile(url):
            return
        content = ArticleUtils.removeAllTag(item["content"])
        referer = item["referer"]
        if not ArticleUtils.isSameSite(referer,url):
            return
        postiveItem = 0  # 标示爬取是否成功（content是否有内容）
        if StringUtils.isNotEmpty(content):
            postiveItem = 1
        timestamp = item["timestamp"]
        parse = item["parse"]
        # condition = {'seed': referer, 'time': item["timestamp"]}
        id =  ArticleUtils.getArticleId(referer+"_"+parse+"_0_"+str(item["crawlId"]))
        oldCs = self.crawlStat.find_one({'_id':id})
        html = oldCs["html"]
        if len(item['html']) > len(oldCs['html']):
            html = item['html']
        self.crawlStat.find_one_and_update({'_id':id}, {'$inc': {'all': 1,'success': postiveItem}, '$set': {'time': timestamp,"html": html}})

    def saveCrawlStat(self, url,crawlId,crawlName, timestamp,parse="detail",html="",depthNumber=0):
        id = ArticleUtils.getArticleId(url+"_"+parse+"_"+str(depthNumber)+"_"+str(crawlId))
        html = html
        if depthNumber >=1:
            oldCs = self.crawlStat.find_one({'_id':id})
            if oldCs is not None and "html" in oldCs:
                if len(oldCs['html']) > len(html):
                    html = oldCs['html']
        self.crawlStat.save({'_id':id,'seed': url, 'crawlId':crawlId,'crawlName':crawlName,"time": timestamp, "all": 0,"depthNumber":depthNumber, "success": 0,
                                "html": html,"parse":parse})


    def get_crawl_stat(self,crawlId,parse="detail",depthNumber=0):

        return self.crawlStat.find({"parse": parse,"depthNumber":depthNumber,"crawlId":crawlId})


    def save_compare_result(self,compare_result):
        compare_result['updateAt'] = TimeUtils.getNowMill()
        self.comparison.save(compare_result)



    def get_baseline(self,id):
        return self.baseline.find_one({"_id":id})

    def save_baseline(self, baseline):
        baseline['updateAt'] = TimeUtils.getNowMill()
        self.baseline.save(baseline)