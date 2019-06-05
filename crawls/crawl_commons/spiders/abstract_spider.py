# @Date:   12-Mar-2019
# @Email:  Tang@jeffery.top
# @Filename: abstract_spider.py
# @Last modified time: 26-Mar-2019



from crawl_commons.items import CrawlResultItem
from crawl_commons.repository.seed import *
from crawl_commons.repository.crawl import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.string_util import *
from crawl_commons.utils.http_util import *
import scrapy
import logging
import time
from crawl_commons.monitor.template_monitor import TemplateComparator


class AbstractSpider(object):

    def __init__(self,crawl_name):
        self.LOG = logging.getLogger("abstractSpider")
        self.spiderName = crawl_name
        self.crawlName = crawl_name.replace("history_", "")
        self.isHistory = ArticleUtils.isHistory(self.spiderName)
        self.isStat = ArticleUtils.isStat(self.spiderName)
        self.crawlId = 0
        self.seedDB = SeedRepository()
        self.crawlDB = CrawlRepository()
        self.crawlId = self.seedDB.get_crawl_id(self.crawlName)
        self.LOG.info("crawlId=%d crawlName=%s isHistory=%s" % (self.crawlId,self.crawlName,self.isHistory))
        self.templateComparator = TemplateComparator(self.crawlDB)

    def do_start_requests(self):  # 由此方法通过下面链接爬取页面
        seeds_meta = self.get_seeds()
        for seed_meta in seeds_meta:
            url = seed_meta["seedInfo"].url
            yield self.do_request(url=url,meta=seed_meta,cleanup=True)
            # yield scrapy.Request(url=url, meta=seed_meta, callback=self.parse)


    def get_seeds(self,isRegex=True):
        seeds = self.seedDB.get_seed_crawlId(self.crawlId)
        timestamp = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))  # 该次爬虫的时间戳
        # 定义爬取的链接
        for seed in seeds:
            # if seed.url != 'http://www.gzdis.gov.cn/xwhc/gzrbzk/':
            #     continue
            # if 'xuexi' not in seed.url:
            #     continue
            regex = self.seedDB.get_regex(seed.regexName)
            if isRegex and (regex is None or len(regex)<=0):
                self.LOG.infog("%s no regex" % seed.url)
                continue
            if self.isStat:
                self.crawlDB.saveCrawlStat(seed.url, self.crawlId, self.crawlName, timestamp,"detail")  # 初始化种子统计
            meta = {}
            meta["timestamp"] = timestamp
            meta["seedRegex"] = regex
            meta["depthNumber"] = 0
            meta["pageNumber"] = 1
            meta["seedInfo"] = seed
            meta["renderType"] = seed.renderType
            # meta["renderType"] = 0
            meta["pageRenderType"] = seed.pageRenderType
            meta["renderSeconds"] = seed.renderSeconds
            meta["nocontentRender"] = seed.nocontentRender
            meta['is_Nextpage'] = False
            yield meta


    def do_parse_list_regex(self, response):
        meta = response.meta
        pageNumber = meta["pageNumber"]
        regexList = meta["seedRegex"]
        seed = meta["seedInfo"]
        depthNumber = int(meta["depthNumber"])
        regexDict = regexList[depthNumber].regexDict
        jsdata = ''
        if pageNumber <=1 and self.isStat:
            html = "".join(response.xpath("//html").extract())
            self.crawlDB.saveCrawlStat(seed.url,self.crawlId,self.crawlName, meta["timestamp"], "list",html,depthNumber)
        if "list" not in regexDict:
            self.log("%s no list regex" % response.url)
            yield
        if regexDict['list'][-1].regexType == 'json':
            jsdata = ArticleUtils.getJsonContent(response)
            if jsdata == '':
                self.log("%s no json regex failed" % response.url)
        listRegexs = regexDict["list"]
        # domain = meta["seedInfo"].domain
        listDataAll = {}
        detailUrls = []
        # self.log(response.text)
        # self.log(regexDict['list'][-1])
        if regexDict['list'][-1].regexType == 'json':
            detailUrls = ArticleUtils.getResponseJsonFieldValue('list',listRegexs,jsdata)
            for (k, v) in regexDict.items():
                if "nextPage" == k or "list" == k:
                    continue
                itemValues = ArticleUtils.getResponseJsonFieldValue(k, v, jsdata)
                listDataAll[k] = itemValues
        else:
            detailUrls = ArticleUtils.getResponseContents4WebRegex(listRegexs, response)
            for (k, v) in regexDict.items():
                if "nextPage" == k or "list" == k:
                    continue
                itemValues = ArticleUtils.getResponseFieldValue(k, False, v, response)
                listDataAll[k] = itemValues
        listRegex = listRegexs[-1]
        # print(detailUrls)
        # self.log(itemValues)
        isDetail = True
        if depthNumber + 1 < regexList[-1].depthNumber:
            isDetail = False
        for i, detailUrl in enumerate(detailUrls):
            isVaildUrl = True
            if StringUtils.isNotEmpty(listRegex.resultFilterRegex):
                isVaildUrl = re.match(listRegex.resultFilterRegex, detailUrl)
            if not isVaildUrl:
                continue
            targetUrl = ArticleUtils.getFullUrl(detailUrl, response.url)
            if ArticleUtils.isErrorUrl(targetUrl):
                continue
            if depthNumber == 0:
                targetUrl = ArticleUtils.getFullUrl(detailUrl, seed.url)
            self.LOG.info("isDetail %s targetUrl %s" % (str(isDetail), targetUrl))
            # if domain not in targetUrl:
            #     continue
            listData = {}
            metaCopy = meta.copy()
            if "listData" in meta and len(meta["listData"]) > 0:
                listData = meta["listData"]
            for (k, v) in listDataAll.items():
                if v is not None and i < len(v) and v[i] is not None and StringUtils.isNotEmpty(str(v[i])):
                    listDataValue = v[i]
                    if "category" == k and k in listData:
                        listDataValue = listData["category" + "/" + listDataValue]
                    listData[k] = listDataValue
            metaCopy["listData"] = listData
            metaCopy["contentPageNumber"] = 1
            metaCopy["depthNumber"] = depthNumber + 1
            metaCopy["refererLink"] = response.url
            metaCopy["renderType"] = listRegex.renderType
            metaCopy["pageRenderType"] = listRegex.pageRenderType
            metaCopy["renderSeconds"] = listRegex.renderSeconds
            if 'publishAt' in listData:
                metaCopy["anchorTime"] = listData['publishAt']
            if 'title' in listData:
                metaCopy["anchorText"] = listData['title']
            # metaCopy["renderBrowser"] = listRegex.renderBrowser
            if ArticleUtils.isFile(targetUrl):
                self.crawlDB.saveFileCrawlDetail(metaCopy, targetUrl)
            elif isDetail:
                metaCopy['parse'] = 'detail'
                yield self.do_request(url=targetUrl,meta=metaCopy)
                # yield scrapy.Request(url=targetUrl, meta=metaCopy, callback=self.parseDetail)
            else:
                self.LOG.info("next level %s" % targetUrl)
                # yield scrapy.Request(url=targetUrl, meta=metaCopy, callback=self.parse)
                yield self.do_request(url=targetUrl, meta=metaCopy,cleanup=True)


        maxPageNumber = 0
        nextPageRegex = []
        if "nextPage" in regexDict:
            nextPageRegex = regexDict["nextPage"]
            maxPageNumber = nextPageRegex[-1].maxPageNumber
        if self.isHistory and ((maxPageNumber > 0 and pageNumber <= maxPageNumber) or maxPageNumber <= 0):
            meta["pageNumber"] = pageNumber + 1
            nextUrls = ArticleUtils.getNextPageUrl(nextPageRegex, response,meta["pageNumber"])
            if len(nextUrls) > 0 and StringUtils.isNotEmpty(nextUrls[0]):
                targetNextUrl = nextUrls[0]
                self.LOG.info("nextPage %s" % targetNextUrl)
                yield self.do_request(url=targetNextUrl, meta=meta)
                # yield scrapy.Request(url=targetNextUrl, meta=meta, callback=self.parse)
            else:
                self.LOG.info("lastPage %s" % (response.url))


    def do_request(self,url, meta,dont_filter=False,cleanup=False):
        if "parse" in meta and meta["parse"] == "detail" :
            return scrapy.Request(url=url, meta=meta, callback=self.parseDetail,dont_filter=dont_filter)
        else:
            return scrapy.Request(url=url, meta=meta, callback=self.parse,dont_filter=dont_filter)



    def do_parse_detal_regex(self, response):
        meta = response.meta
        url = response.url
        regexList = meta["seedRegex"]
        regexDict = regexList[-1].regexDict
        seed = meta["seedInfo"]
        listData = {}
        if "listData" in meta:
            listData = meta["listData"]
        enableDownloadFile = False
        enableDownloadImage = False
        enableSnapshot = False
        nocontentRender = meta["nocontentRender"]
        contentPageNumber = meta["contentPageNumber"]
        if seed.enableDownloadFile == 1:
            enableDownloadFile = True
        if seed.enableDownloadImage == 1:
            enableDownloadImage = True
        if seed.enableSnapshot == 1:
            enableSnapshot = True
        detailData = {}
        if "detailData" in meta:
            detailData = meta["detailData"]
        if contentPageNumber <= 1:
            detailData["url"] = url
        autoDetailData = {}
        if "autoDetailData" in meta:
            autoDetailData = meta["autoDetailData"]

        contentAutoData = None
        html = "".join(response.xpath("//html").extract())
        meta["autoDetailData"] = autoDetailData
        maxPageNumber = 0
        pageContent = ""
        pageContentImages = None
        contentData = {}
        if enableDownloadFile:
            files = ArticleUtils.getContentFiles(response)
            if files is not None and len(files) > 0:
                contentData["contentFiles"] = files
                # ArticleUtils.mergeDict(detailData, "contentFiles", files)

        for (k, v) in regexDict.items():
            if "nextPage" == k:
                continue
            itemValues = ArticleUtils.getResponseFieldValue(k, True, v, response)
            itemValue = None
            if itemValues is not None and len(itemValues) > 0 and itemValues[0] is not None and StringUtils.isNotEmpty(StringUtils.trim(str(itemValues[0]))):
                itemValue = itemValues[0]
            if itemValue is None:
                continue
            contentData[k] = itemValue
            if "content" == k:
                pageContent = ArticleUtils.removeAllTag(itemValue)
                maxPageNumber = v[-1].maxPageNumber
                images = ArticleUtils.getContentImages(v, response)
                if images is not None and len(images) > 0:
                    contentData["contentImages"] = images
                    pageContentImages = images

                        # ArticleUtils.mergeDict(detailData,"contentImages",images)
                contentSnapshots = ArticleUtils.getResponseFieldValue("contentSnapshot", True, v, response)
                if contentSnapshots is not None and len(contentSnapshots) > 0 and StringUtils.isNotEmpty(contentSnapshots[0]):
                    if enableSnapshot:
                        contentData["contentSnapshot"] = contentSnapshots[0]
                        # ArticleUtils.mergeDict(detailData,"contentSnapshot",contentSnapshots[0])

        if StringUtils.isEmpty(pageContent) and pageContentImages is None:
            if contentAutoData is None:
                contentAutoData = ArticleUtils.getAutoDetail(contentPageNumber, html, enableDownloadImage,enableSnapshot)
            if "contentImages" in contentAutoData:
                pageContentImages = contentAutoData["contentImages"]
            if "content" in contentAutoData:
                pageContent = ArticleUtils.removeAllTag(contentAutoData["content"])


        if StringUtils.isEmpty(pageContent) and pageContentImages is None and nocontentRender == 1 and not ArticleUtils.isRender(meta, self.name):
            metaCopy = meta.copy()
            metaCopy["renderType"] = 1
            metaCopy["renderSeconds"] = 5
            metaCopy["detailData"] = detailData
            metaCopy["autoDetailData"] = autoDetailData
            self.LOG.info("re render url %s" % url)
            yield self.do_request(url=url,meta=metaCopy,dont_filter=True,cleanup=True)
            # 获取不到正文，尝试使用js渲染方式，针对网站部分链接的详情页使用js跳转
            # yield scrapy.Request(url=url, meta=metaCopy, callback=self.parseDetail, dont_filter=True)
        else:
            ArticleUtils.mergeNewDict(detailData, contentData)

            if contentPageNumber <=1 and "publishAt" not in detailData and "publishAt" not in autoDetailData and "publishAt" not in listData:
                autoDetailData["publishAt"] = TimeUtils.get_conent_time(html,-1)
            if contentAutoData is None and (("title" not in detailData and "title" not in listData) or (StringUtils.isEmpty(pageContent)) and pageContentImages is None):
                contentAutoData = ArticleUtils.getAutoDetail(contentPageNumber,html, enableDownloadImage, enableSnapshot)
            ArticleUtils.mergeNewDict(autoDetailData, contentAutoData)


            # with open(file="/home/yhye/tmp/crawl_data_policy/" + ArticleUtils.getArticleId(response.url) + ".html", mode='w') as f:
            #     f.write("".join(response.xpath("//html").extract()))

            nextPageRegex = []
            if "nextPage" in regexDict:
                nextPageRegex = regexDict["nextPage"]
                maxPageNumber = nextPageRegex[-1].maxPageNumber
            targetNextUrl = ""
            if maxPageNumber <= 0 or (maxPageNumber > 0 and contentPageNumber < maxPageNumber):
                meta["contentPageNumber"] = contentPageNumber + 1
                nextUrls = ArticleUtils.getNextPageUrl(nextPageRegex, response,meta["contentPageNumber"])
                if len(nextUrls) > 0 and StringUtils.isNotEmpty(nextUrls[0]):
                    targetNextUrl = nextUrls[0]
            #防止死循环翻页
            if StringUtils.isNotEmpty(targetNextUrl) and contentPageNumber <= 100:
                meta["detailData"] = detailData
                meta["autoDetailData"] = autoDetailData
                self.LOG.info("detail nextPage %s %s" % (str(contentPageNumber + 1), targetNextUrl))
                yield self.do_request(url=url, meta=meta,dont_filter=False,cleanup=True)
                # yield scrapy.Request(url=targetNextUrl, meta=meta, callback=self.parseDetail)
            else:
                item = ArticleUtils.meta2item(meta, detailData["url"])
                for (k, v) in detailData.items():
                    itemValue = None
                    if "category" == k and k in item:
                        itemValue = item[k] + "/" + v
                    elif "contentImages" == k or "contentFiles" == k:
                        itemValue = json.dumps(list(v.values()), ensure_ascii=False)
                    else:
                        itemValue = v
                    item[k] = itemValue
                detailImages = None
                if "contentImages" in detailData:
                    detailImages = detailData["contentImages"]
                for (k, v) in autoDetailData.items():
                    if detailImages is not None and ("content" == k or "contentSnapshot" == k):
                        continue
                    if "contentImages" == k and k not in item:
                        item[k] = json.dumps(list(v.values()), ensure_ascii=False)
                    elif k not in item or StringUtils.isEmpty(ArticleUtils.removeAllTag(str(item[k]))):
                        item[k] = v

                item["headTitle"] = StringUtils.trim(ArticleUtils.removeAllTag("".join(response.xpath("//title//text()").extract())))
                if "title" not in item or StringUtils.isEmpty(item["title"]):
                    item["title"] = ArticleUtils.cleanHeadTitle(item["headTitle"])
                item["html"] = html
                yield item

    def do_closed(self,reason):
        self.LOG.info("on close start stat seeds %s %s" % (self.crawlId,self.crawlName))
        self.LOG.info(reason)
        if self.crawlId > 0:
            self.seedDB.stat_seed(self.crawlId)
            if "auto_" not in self.crawlName and "test_" not in self.crawlName and not self.isHistory:
                self.templateComparator.run_task(self.crawlId)

        self.LOG.info("%s %s stat seeds finished" % (self.crawlId,self.name))
