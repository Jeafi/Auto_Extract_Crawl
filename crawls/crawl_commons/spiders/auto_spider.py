from readability import Document
from newspaper import Article
import scrapy
import xlrd
import time
import re
from urllib.parse import urljoin
import jieba
import json
from crawl_commons.spiders.abstract_spider import AbstractSpider
from crawl_commons.items import CrawlResultItem
from crawl_commons.repository.seed import *
from crawl_commons.repository.crawl import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.string_util import *
from crawl_commons.utils.time_util import *


# 一级页面抓取通用爬虫，该爬虫不作爬取


class AutoSpider(scrapy.Spider, AbstractSpider):  # 需要继承scrapy.Spider类
    name = "auto_spider"  # 定义蜘蛛名
    restrictNewspaper = [
        'http://bxjg.circ.gov.cn/web/site0/tab5241/',
        'http://www.szse.cn/lawrules/service/servicedirect/t20181228_565063.html'
    ]
    restrictContentTitle = [
        'http://www.gzcz.gov.cn',
        'http://www.gzdpc.gov.cn'
    ]

    def __init__(self, name=None, **kwargs):
        scrapy.Spider.__init__(self, name=name, kwargs=kwargs)
        AbstractSpider.__init__(self, self.name)
        # super(AutoSpider, self).__init__(name=name, kwargs=kwargs)
        # self.seedDB = SeedRepository()
        # self.crawlDB = CrawlRepository()

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        return self.do_start_requests()

    def parse(self, response):
        '''起始页面解析'''
        # 起始页面url抽取'''
        meta = response.meta
        start_url = meta["seedInfo"].url
        meta['newspaper'] = False
        if start_url in self.restrictNewspaper:
            meta['newspaper'] = True
        link_list = self.get_list_urls(start_url, response)
        self.log(link_list)
        for url in link_list.keys():
            if not ArticleUtils.isSameSite(start_url,url):
                continue
            metaCopy = meta.copy()
            for resUrl in self.restrictContentTitle:
                if ArticleUtils.isSameSite(resUrl, start_url):
                    metaCopy['anchorText'] = ''
                else:
                    metaCopy['anchorText'] = ArticleUtils.clearListTitle(link_list[url][0])
            metaCopy['anchorTime'] = link_list[url][1]
            metaCopy['parse'] = 'detail'
            metaCopy["contentPageNumber"] = 1
            if not ArticleUtils.isFile(url):
                yield self.do_request(url=url, meta=metaCopy)
            else:
                listData = {"title":metaCopy['anchorText'],"publishAt":metaCopy['anchorTime']}
                metaCopy['listData'] = listData
                self.crawlDB.saveFileCrawlDetail(metaCopy, url)
                # item = self.parseFileurl(url=url, meta=metaCopy)
                # self.crawlDB.saveCrawlDetail(item)
            # yield scrapy.Request(url=url, meta=meta, callback=self.parseDetail)
        if self.isHistory:
            # 如果有下一页,爬下一页
            meta["pageNumber"] = meta["pageNumber"]+1
            nextpage_urls = ArticleUtils.getNextPageUrl('', response,  meta["pageNumber"])
            for url in nextpage_urls:
                self.log("nextPage %s" % url)
                meta['is_Nextpage'] = True
                yield self.do_request(url=url, meta=meta, cleanup=True)
                # yield scrapy.Request(url=url, meta=meta, callback=self.parse)

    def parseDetail(self, response):
        '''
        详情页解析
        '''
        meta = response.meta
        url = response.url
        seed = meta["seedInfo"]
        enableDownloadFile = False
        enableDownloadImage = False
        enableSnapshot = False
        if seed.enableDownloadFile == 1:
            enableDownloadFile = True
        if seed.enableDownloadImage == 1:
            enableDownloadImage = True
        if seed.enableSnapshot == 1:
            enableSnapshot = True
        detailData = {}
        html = "".join(response.xpath("//html").extract())
        doc = Document(html)  # 利用readabilty处理文件
        if "detailData" in meta:
            detailData = meta["detailData"]
        if len(detailData) <= 0:
            # '''是否用readabilty的title'''
            # detailData["title"] = doc.title()  # 详情第一页时读入标题和url
            # if len(detailData["title"]) <= len(meta['anchorText']):
            #     detailData["title"] = meta['anchorText']
            detailData["title"] = meta['anchorText'].strip()
            if detailData["title"].find('...') != -1 or detailData["title"] == '':
                detailData["title"] = ArticleUtils.cleanHeadTitle(doc.title())
            if 'anchorTime' in meta and meta['anchorTime'] > 0:
                detailData["publishAt"] = meta['anchorTime']
            if "publishAt" not in detailData:
                detailData["publishAt"] = TimeUtils.get_conent_time(html,0)
            # if detailData["publishAt"] == '':
            #     ts = time.strptime(meta["timestamp"], "%Y-%m-%d %H-%M-%S")
            #     ts = int(time.mktime(ts)) * 1000
            #     detailData["publishAt"] = ts
            detailData["url"] = url
        content_snap = doc.summary()
        useNewspapaer = False  # 是否使用了newspaper
        if len(ArticleUtils.removeTag4Content(content_snap).strip()) < 3 or meta['newspaper']:
            article = Article(response.url, language='zh', keep_article_html=True, fetch_images=False)
            article.download(input_html=response.text)
            article.parse()
            content = article.text
            content_snap = article.article_html
            useNewspapaer = True
        # 获取正文
        if useNewspapaer == False:
            content = ArticleUtils.removeTag4Content(content_snap)  # 如果没用newspaper，将快照去标签作正文
        ArticleUtils.mergeDict(detailData, "content", content)
        if enableDownloadImage:
            images = ArticleUtils.get_content_image_urls(content_snap, url)
            if images is not None and len(images) > 0:
                ArticleUtils.mergeDict(detailData, "contentImages", images)
        if enableDownloadFile:
            files = ArticleUtils.getContentFiles(response)
            if files is not None and len(files) > 0:
                ArticleUtils.mergeDict(detailData, "contentFiles", files)
        if enableSnapshot:
            ArticleUtils.mergeDict(detailData, "contentSnapshot", content_snap)
        # 爬取下一页
        contentPageNumber = meta["contentPageNumber"]
        nextpage_urls = []
        if  contentPageNumber < 100:
            meta["contentPageNumber"] = contentPageNumber + 1
            nextpage_urls = ArticleUtils.getNextPageUrl('', response,meta["contentPageNumber"])
        if len(nextpage_urls) != 0:
            meta["detailData"] = detailData
            yield scrapy.Request(url=nextpage_urls, meta=meta, callback=self.parseDetail)
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
            item['html'] = html
            item["headTitle"] = StringUtils.trim(
                ArticleUtils.removeAllTag("".join(response.xpath("//title//text()").extract())))
            yield item

    def get_list_urls(self, starturl, response):
        minNumZero = [
            'http://www.gzcz.gov.cn',
            'http://www.gzdpc.gov.cn',
            'http://www.gzdis.gov.cn',
            'http://www.anshun.gov.cn',
            'guizhou.gov.cn'
        ]
        print('*******************************************')
        print(starturl)
        '''
        从初始页面中提取列表url
        @param starturl：初始url
        @parm response
        @return url 字典{url：锚文本}
        '''
        a_tags = response.xpath('//a')
        print('-------------------------------')
        print('所有的链接数目', len(a_tags))

        href_parent = self.getSameParent(starturl, a_tags, fine=False)
        onlyFlag =True
        minNum = 1
        for resUrl in minNumZero:
            if ArticleUtils.isSameSite(resUrl, starturl):
                onlyFlag = False
                minNum = 0
        # print(onlyFlag+minNum)
        final_urls = self.listFilter(href_parent, 10.8, 5.5, only= onlyFlag, max=False, minNum = minNum)
        print('过滤后的链接数目', len(final_urls))
        if len(final_urls) == 0:
            final_urls = self.listFilter(href_parent, 10.8, 5.5, only= onlyFlag, max=True, minNum = minNum)
            print('max过滤后的链接数目', len(final_urls))
        return final_urls

    def removeNum(self,str):
        '''
        去除字符串里面的数字
        '''
        a = filter(lambda x: x.isalpha(), list(str))
        b=list(a)
        return ''.join(b)

    def listFilter(self, href_parent, averageLength, averageWordCounts, only, max, minNum):
        '''
        列表筛选
        @
        @averageLength:阈值平均长度
        @averageWordCounts：阈值平均字数
        @only：是否只去一个列表页
        @max:是否允许在没有符合要求数据时，取平均长度最长列表
        @return：urls
        '''
        listList = []  # 列表的列表
        fibbdenchars =[10.375,10.1875] # 禁用的字数，重构后用静态
        fibbdentree =[r"lifloatleftwidthpxulwidthpxpositionrelativeoverflowhiddenpaddingpxmarginpxleftpxdivtempWrapdivzytsnrdivzytsdivnavbodyNonehtmlhttpwwwworgxhtml",
        r"spanfloatleftheightpxlineheightpxpaddingrightpxdivwidthpxheightpxmarginautopaddingdivfrdivdibxxdivfootbodyNonehtmlhttpwwwworgxhtml",
        "tdtoptrNonetbodyNonetabletdmiddletrNonetbodyNonetablemarginautodivmainfootbodyNonehtmlhttpwwwworgxhtml",
        "hheightpxlineheightpxpaddingtoppxlifixcurulfixewmdivfixedboxbodyNonehtmlhttpwwwworgxhtml",
        "spancnzzstaticonpdisplaynonedivsyqtdivfooterbodyNonehtmlhttpwwwworgxhtml"
        "liNoneuldiyselectlistdivselectlistdivdiyselectformNonedivconselectdivlinkdivMaindivwarpbodyNonehtmlNone", # 安顺
        "liNoneuldiyselectlistdivselectlistdivdiyselectformNonedivconselectdivlinkdivFooterautomtdivwarpbodyScrollStylehtmlNone", 
        "pNonedivfootTexBoxfldivwBoxautotransitiondofdivFooterautomtdivwarpbodyScrollStylehtmlNone",#  贵州监察
        "divNonedivztdivnavnrdivnavboxdivnavldivleftleftboxdivcontaindivcontainerbodyNonehtmlhttpwwwworgxhtml",
        "divNonedivContentlistsdivContentlistsdivContentlistdivzpdivnavnrdivnavboxdivnavldivleftleftboxdivcontaindivcontainerbodyNonehtmlhttpwwwworgxhtml",
        "divNonedivContentlistdivzpdivnavnrdivnavboxdivnavldivleftleftboxdivcontaindivcontainerbodyNonehtmlhttpwwwworgxhtml",
        "divNonedivContentlistsdivContentlistdivzpdivnavnrdivnavboxdivnavldivleftleftboxdivcontaindivcontainerbodyNonehtmlhttpwwwworgxhtml", #  安徽省
        "pNonedivNonedivlefttextdivfootercondivfooterdivwarpbodyNonehtmlNone",
        "liNoneulNonedivqggdgbcxcondivleftcondivmaincdivmaindivwarpbodyNonehtmlNone", #  贵州省政府公报
        "liNoneulNonedivyqljcondivlinkdivfooterbodyNonehtmlhttpwwwworgxhtml" #  贵州省商务厅
        "liNoneuldiyselectlistdivselectlistdivdiyselectformNonedivconselectdivlinkdivMaindivwarpbodyNonehtmlNone", #安顺人民政府
        "spanjspeechpNonedivfootconfldivfootdivfooterbodyNonehtmlNone" #  http://www.ahtjj.gov.cn/tjjweb/web/list.jsp?strWebSiteId=13781720451562390&strColId=13786945245845740&strColId2=f1e311c6c10e4f3d835a485e704d3404
        
        ]
        allowedtree =[r"liNoneulNonedivxxlbdivfrdivcontentbodyNonehtmlhttpwwwworgxhtml",
        "ulNonedivbddivgbslideTxtBoxdivleftleftBoxdivmainBoxbodyNonehtmlzhCN", #  宁夏
        "liNonedivgbqsdivrightcondivmaincdivmaindivwarpbodyNonehtmlNone", #  贵州省政府公报
        "tdfffffftrNonetabletdtrNonetbodyNonetabledivmainbodybackgroundurlTMPimagesbodybgjpgcentertoprepeatyfffhtmlhttpwwwworgxhtml", #  安徽省人民政府公报
        "liNoneulNonedivNewsListdivybnrfrdivmaindivMainwBoxautodivwarpbodyScrollStylehtmlNone", #  http://www.gzdis.gov.cn/djfg/dnfgzd/dz/
        "liNoneulNonedivNewsListdivybnrfrdivtabcondivzxmenucondivMaindivwarpbodyNonehtmlNone" # 安顺幼儿园
        ]
        maxLength = 0
        maxName = ''
        for father_node in href_parent.keys():
            urls = dict()
            child_count = 0
            child_total_length = 0
            word_count = 0
            print('------------------------')
            for child_tag, text, length, href, _ in href_parent[father_node]:
                child_count += 1
                child_total_length += len(text.strip())
                word_count += len(" ".join(jieba.cut(text.strip())).split(" "))
                # 链接描述平均字数和次数都大于阈值
                print(text.strip(), '|', href)
            averageChildLength = child_total_length / child_count
            averageChildWords = word_count / child_count
            # 记录max
            if (averageChildLength) > maxLength and child_count != 1 and (
                    averageChildLength) not in fibbdenchars:
                maxLength = child_total_length / child_count
                maxName = father_node
            print(father_node, child_count, averageChildLength, averageChildWords)
            # print(self.removeNum(father_node) in allowedtree)
            # print(self.removeNum(father_node) == fibbdentree[0])
            # print(self.removeNum(father_node))
            # print(self.removeNum(fibbdentree[0]))
            if (averageChildLength > averageLength and averageChildWords > averageWordCounts and child_count > minNum) or self.removeNum(father_node) in allowedtree:
                if self.removeNum(father_node) not in fibbdentree:
                    print("ture")
                    for _, text, _, href, time in href_parent[father_node]:
                        urls[href] = [text, time]
                    listList.append(urls)
        print('-------------------------------')
        final_list = dict()
        if max is True:
            for _, text, _, href, time in href_parent[maxName]:
                final_list[href] = [text, time]
            return final_list
        if only is True:
            for l in listList:
                if len(l) > len(final_list):
                    final_list = l
            return final_list
        else:
            for l in listList:
                final_list.update(l)
            return final_list

    def getSameParent(self, starturl, a_tags, fine):
        '''
        获取拥有统一父标签的链接字典
        @a_tags：a标签
        @fine:精细模式
        @return：href_parent字典，（父节点名称：【urls】）
        '''
        href_parent = dict()
        if fine is True:
            i = 0
            lastname = ''
        for a_tag in a_tags:
            # 抽取href，过滤掉无效链接
            href = a_tag.xpath('@href').extract_first()
            if href is None:
                continue
            if 'javascript:openUrl' in href:
                # print(href)
                href = href.split('(')[1].strip(')').strip('\'')

            # 获取a标题文本内容，无内容的链接不抓取
            texts = a_tag.xpath('text()').extract()
            # onmouseout http://www.sc.gov.cn/10462/cwh/cwhhg/cwhhg.shtml
            text = ''.join(texts)
            if text is None or len(text.strip()) == 0:
                texts = a_tag.xpath('@title').extract()
                text = ''.join(texts)
                if text is None or len(text.strip()) == 0:
                    texts = a_tag.xpath('li/text()').extract()
                    text = ''.join(texts)
                    if text is None or len(text.strip()) == 0:
                        continue

            # 相对地址绝对化
            if 'http' not in href:
                href = urljoin(starturl, href)

            # 获取时间
            if starturl.find('mohurd') > 0:
                timeInfo = a_tag.xpath('../../.').extract()
            else:
                timeInfo = a_tag.xpath('../text()|../span').extract()
            time = ''
            for t in timeInfo:
                time = time + t
            # print(time)
            # print('*'*20)
            time = TimeUtils.get_conent_time(time,0)
            # print (time)

            # 获取父节点
            treePath = ''
            father_tag = a_tag.xpath('..')
            while father_tag.xpath('local-name(.)').extract_first() is not None:
                treePath = treePath + str(father_tag.xpath('local-name(.)').extract_first())
                if (father_tag.xpath('@*') is not None):
                    treePath = treePath + self.classExtract(father_tag.xpath('@*').extract_first())
                father_tag = father_tag.xpath('..')

            father_name = treePath
            if father_name is not None:
                father_name = '<' + father_name
                for index, attribute in enumerate(father_tag.xpath('@*'), start=0):
                    attribute_name = father_tag.xpath('name(@*[%d])' % index).extract_first()
                    father_name += ' ' + attribute_name + "=" + attribute.extract()
                father_name += '>'
                if fine is True:
                    if father_name not in href_parent:
                        lastname = father_name
                        href_parent[father_name] = [(a_tag, text, len(text), href, time)]
                        print(father_name + ":" + href)
                    elif father_name == lastname or lastname.endswith(father_name) == True:
                        href_parent[lastname].append((a_tag, text, len(text), href, time))
                        print(lastname + ":" + href)
                    else:
                        father_name = str(i) + father_name
                        i = i + 1
                        href_parent[father_name] = [(a_tag, text, len(text), href, time)]
                        print(father_name + ":" + href)
                        lastname = father_name
                else:
                    if father_name not in href_parent:
                        href_parent[father_name] = [(a_tag, text, len(text), href, time)]
                    else:
                        href_parent[father_name].append((a_tag, text, len(text), href, time))
        return href_parent

    def classExtract(self, xpath):
        '''在这里加规则增加列表识别的适配性'''
        '''基金协会适配'''
        if str(xpath).startswith('newsList'):
            return 'None'
        ''' 中国政府网适配 '''
        if str(xpath) == 'line':
            return 'None'
        return self.removeNum(str(xpath))

    def closed(self, reason):
        self.do_closed(reason)
