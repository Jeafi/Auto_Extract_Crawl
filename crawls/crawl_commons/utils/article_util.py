# @Date:   12-Mar-2019
# @Email:  Tang@jeffery.top
# @Filename: article_util.py
# @Last modified time: 26-Mar-2019



# -*- coding: utf-8 -*-

import re
import hashlib
from crawl_commons.items import CrawlResultItem
from crawl_commons.utils.string_util import *
from crawl_commons.utils.time_util import *
from crawl_commons.repository.seed import *
from crawl_commons.repository.crawl import *
from urllib.parse import *
from readability import Document
import copy


class ArticleUtils(object):

    FILE_PATTERN = re.compile(u'.*?\.(pdf|doc|xls|xlsx|docx|pptx|ppt|)$')
    FILE_POSTFIXS = [".pdf",".doc",".xls",".xlsx",".docx",".pptx",".ppt",".PDF",".DOC",".XLS",".XLSX",".DOCX",".PPTX",".PPT"]
    MERGE_FIELD = ["content","contentImages","contentFiles","contentSnapshot"]
    PAGE_CONTENT = [">上页<", ">上一页<", ">下页<", ">下一页<",">末页<",">尾页<",">首页<"]
    COMMON_NEXT_PAGE_REGEX = [WebRegex({"regexType":"xpath","regexField":"nextPage", "regexContent":'//a[contains(text(),"下一页") or contains(text(),"下页") or contains(text(),"后一页") or text()=">" ]//@href',"resultFormat":"","pageRenderType":0,"renderSeconds":"0","renderType":"0","renderBrowser":"","regexSort":"0","depthNumber" :"0","resultFilterRegex":"","maxPageNumber":"0"})]
    ERROR_PAGE_PATTERN = re.compile(u'.*?(404|服务器错误|页面找不到|页面没有找到|no-title).*')
    ERROR_PAGE_TITLE_PATTERN = re.compile(u'.*?(首页|末页|上一页|下一页|上页|下页|尾页|后一页|前一页).*')

    ERROR_PAGE_CONTENT_PATTERN = re.compile(u'.*?(页面已删除|请开启JavaScript|页面不存在|资源可能已被删除|请用新域名访问|BadGateway|BadRequest|ErrorPage).*')

    ERROR_URL_PATTERN = re.compile(u'^((?!www.gov.cn/zhuanti/|www.china.com.cn/zhibo/).)*$')

    @classmethod
    def removeTag4Content(cls, str):
        if str is None:
            return u""
        dd = str
        dd = dd.replace("&#13;","<br>")
        #<div>作为段落标准的文章
        if "</p>" not in str and "</div>" in str:
            drPre = re.compile(u'<div.*?>')
            dd = drPre.sub(u"<p>", dd)
            drPre2 = re.compile(u'</div>')
            dd = drPre2.sub(u"</p>", dd)
        dr0 = re.compile(u'<script.*?>.*?</script>',re.S)
        dd = dr0.sub("",dd)
        dr00 = re.compile(u'</body>', re.S)
        dd = dr00.sub("",dd)
        dr01 = re.compile(u'<body>', re.S)
        dd = dr01.sub("", dd)
        dr02 = re.compile(u'<style.*?>.*?</style>', re.S)
        dd = dr02.sub("", dd)
        dr = re.compile(u'<(?!p|/p|strong|/strong|b|/b)+[^>]+>', re.S)
        dd = dr.sub(u"", dd)
        dd = dd.replace('\n\n', "</p><p>")
        dd = StringUtils.replaceSpecialWords(dd)
        dr2 = re.compile(u'<p.*?>')
        dd = dr2.sub(u"<p>",dd)
        dr3 = re.compile(u'<br.*?>')
        dd = dr3.sub(u"</p><p>",dd)
        dr4 = re.compile(u'<b.*?>')
        dd = dr4.sub(u"<b>", dd)
        dr5 = re.compile(u'<strong.*?>')
        dd = dr5.sub(u"<strong>", dd)
        ddTrim = StringUtils.trim(dd)
        if not ddTrim.startswith("<p>"):
            dd = u"<p>"+dd
        if not ddTrim.endswith("</p>"):
            dd = dd+u"</p>"
        return dd

    @classmethod
    def removeTag4ContentSnapshot(cls, str):
        if str is None:
            return u""
        dr = re.compile(u'<a.*?>')
        dd = dr.sub(u"", str)
        dr2 = re.compile(u'</a>')
        dd = dr2.sub(u"", dd)
        return dd

    @classmethod
    def removeAllTag(cls, str):
        if str is None:
            return u""
        dr = re.compile(u'<[^>]+>', re.S)
        dd = dr.sub(u"", str)
        dd = StringUtils.replaceSpecialWords(dd)
        dd = StringUtils.trim(dd)
        return dd

    @classmethod
    def clearListTitle(cls, listTitle):
        dd = ArticleUtils.removeAllTag(listTitle)
        if dd.startswith("·"):
            dd = dd[1:]
        return dd



    @classmethod
    def getArticleId(cls, url):
        id = hashlib.md5(url.encode(u"utf8")).hexdigest()
        return id

    @classmethod
    def getFullUrl(cls, url,referer):
        urlTmp = url.replace('\n', '')
        urlTmp = urlTmp.replace('\r', '')
        urlTmp = urlTmp.replace('\t', '')
        urlTmp = StringUtils.trim(urlTmp)
        return urljoin(referer,urlTmp)

    @classmethod
    def getSite(cls, url):
        uparse = urlparse(url)
        return uparse.netloc

    @classmethod
    def getDomain(cls, url):
        site = ArticleUtils.getSite(url)
        # print(site)
        siteArr = site.split(".")
        # print(len(siteArr))
        if len(siteArr)<= 3:
            return site
        return ".".join(siteArr[-3:])

    @classmethod
    def isSameSite(cls,referer,url):
        site = ArticleUtils.getSite(url)
        domain = ArticleUtils.getDomain(referer)
        if domain == 'sousuo.gov.cn' and site == 'www.gov.cn':
            return True
        return domain in site

    @classmethod
    def getResponseContents4WebRegex(cls, webRegexs, response):
        contentResponse = response
        for i, regex in enumerate(webRegexs):
            if u"re" == regex.regexType:
                contentResponse = contentResponse.re(regex.regexContent)
            elif u"xpath" == regex.regexType:
                if regex.regexField == "list":
                    contentResponse = contentResponse.xpath(regex.regexContent)
                else:
                    contentResponse = ArticleUtils.getResponseContents4xpath(regex,contentResponse)
        if type(contentResponse) == list:
            return contentResponse
        return contentResponse.extract()

    @classmethod
    def getResponseContents4xpath(cls,xpathRegex,response):
        regexContentArr = xpathRegex.regexContent.split("|")
        contentResponse = None
        for regexContent in regexContentArr:
            contentResponse = response.xpath(regexContent)
            contentResponseExtract = contentResponse.extract()
            if len(contentResponseExtract) <= 0:
                continue
            content = ArticleUtils.removeAllTag("".join(contentResponseExtract))
            if (StringUtils.isEmpty(content)):
                continue
            else:
                break
        return contentResponse

    @classmethod
    def getResponseContents4Contentxpath(cls, xpathRegex, response):
        regexContentArr = xpathRegex.regexContent.split("|")
        contentResponse = None
        for regexContent in regexContentArr:
            contentResponse = response.xpath(regexContent)
            contentResponseExtract = contentResponse.extract()
            if len(contentResponseExtract) <= 0:
                continue
            content = ArticleUtils.removeAllTag("".join(contentResponseExtract))
            images = ArticleUtils.getContentImages4RegexContent(regexContent,response)
            if (StringUtils.isEmpty(content) and (images is None or len(images) <=0)):
                continue
            else:
                break
        return contentResponse

    @classmethod
    def getResponseContents4ContentRegex(cls, webRegexs, response):
        contentResponse = ArticleUtils.getResponseContents4Contentxpath(webRegexs[-1],response).extract()
        contentRemovePage = []
        if len(contentResponse) > 1:
            for i, contentR in enumerate(contentResponse):
                notPage = True
                for pageContent in ArticleUtils.PAGE_CONTENT:
                    if pageContent in contentR:
                        notPage = False
                if notPage:
                    contentRemovePage.append(contentR)
        else:
            contentRemovePage = contentResponse
        return contentRemovePage

    @classmethod
    def getResponseFieldValue(cls,regexField,isOne,webRegexs, response):
        contentResponse = ArticleUtils.getResponseContents4WebRegex(webRegexs,response)
        result = []
        formatter = webRegexs[-1].resultFormat
        if isOne:
            if "content" == regexField or "contentSnapshot" == regexField:
                contentResponse = ArticleUtils.getResponseContents4ContentRegex(webRegexs,response)
            content = "".join(contentResponse)
            result.append(ArticleUtils.getFormatContent(regexField, content, formatter))
        else:
            for content in contentResponse:
                result.append(ArticleUtils.getFormatContent(regexField,content,formatter))
        return result

    @classmethod
    def getJsonContent(cls, response):
        '''
        从response中获得json数据，暂时以学习强国为模板
        @response
        @return 有用的包含json的字串
        '''
        regexfieldsrawdata = "".join(response.xpath("//html").extract())
        # print(regexfieldsrawdata)
        size = len(regexfieldsrawdata)

        count_leftbarckets = 0  # regexfieldsrawdata数据中'['的个数
        count_rightbrackets = count_leftbarckets    # regexfieldsrawdata数据中']'的个数

        index_leftbrackets = -1 # 用来记录regexfieldsrawdata中第一个'['的位置
        index_rightbrackets = -1    # 用来记录regexfieldsrawdata中第一个'['对应']'的位置

        for i in range(size):
            if regexfieldsrawdata[i] == '[':
                count_leftbarckets = count_leftbarckets + 1
                count_rightbrackets = count_leftbarckets 
                if count_leftbarckets == 1:
                    index_leftbrackets = i 
        for i in range(size):
            if regexfieldsrawdata[i] == ']':
                count_rightbrackets = count_rightbrackets - 1
            if count_rightbrackets == 1:
                index_rightbrackets = i
        # 如果遍历完成后，index_leftbrackets保持不变，说明jsonrawdata中没有'['
        if index_leftbrackets == -1:
            print('No regexfields')
        regexfields = regexfieldsrawdata[index_leftbrackets : index_rightbrackets + 2]
        if regexfields[0] == '[' and regexfields[-1] == ']':
            return regexfields
        else:
            return ''

    @classmethod
    def getResponseJsonFieldValue(cls,regexField, webRegexs, jsdata):
        '''
        json按规则取元素
        @regexField:区域名
        @webRegexs：对应规则
        @response
        @starturl:种子链接
        return：该区域内容
        '''
        result = []
        jsdata = json.loads(jsdata)
        for regexfield_temp in jsdata:
            for _webRegex in webRegexs:
                webRegex = _webRegex.regexContent
                regexfield_temp = regexfield_temp[webRegex]
                if "content" == regexField or "contentSnapshot" == regexField:
                #  暂时这么写，正文估计用不着json提取
                    contentResponse = ArticleUtils.getResponseContents4ContentRegex(webRegexs,jsdata)
                if "publishAt" == regexField:
                    regexfield_temp = TimeUtils.convert2Mill4Default(regexfield_temp, "", True)
            # if "list" == regexField and  'http' not in regexfield_temp:
            #     regexfield_temp = urljoin(starturl, regexfield_temp)
                result.append(regexfield_temp)
        return result

    @classmethod
    def getFormatContent(cls, field,content,formatter):
        formatContent = None
        if "content" == field:
            formatContent = ArticleUtils.removeTag4Content(content)
        elif field.endswith("Snapshot"):
            formatContent = ArticleUtils.removeTag4ContentSnapshot(content)
        else:
            trimContent = ArticleUtils.removeAllTag(content)
            trimContent = StringUtils.trim(trimContent)
            if StringUtils.isNotEmpty(formatter):
                formatContent = TimeUtils.convert2Mill4Default(trimContent,formatter,False)
            else:
                formatContent = trimContent
        return formatContent

    @classmethod
    def getMultiPartRegexs(cls, seedRegex):
        seedRegexMultiPart = {}
        for (k, v) in seedRegex.items():
            lastRegex = v[-1]
            if lastRegex.multiPart == 1:
                seedRegexMultiPart[k] = v
        return seedRegexMultiPart

    @classmethod
    def getContentImages(cls,contentRegexs,response):
        contentXPath = None
        for regex in contentRegexs:
            if regex.regexType == "xpath":
                contentXPath = copy.copy(regex)
        if contentXPath is None:
            return None

        regexs = contentXPath.regexContent.split("|")
        regexContent = "//img//@src|".join(regexs) + "//img//@src"
        contentXPath.setRegexContent("contentImages",regexContent)
        images = ArticleUtils.getResponseFieldValue(contentXPath.regexField,False,[contentXPath],response)
        imageDict = {}
        for img in images:
            if StringUtils.isEmpty(img):
                continue
            if img.startswith("data:"):
                continue
            #图片以二进制格式写在网页,不需要下载
            url = ArticleUtils.getFullUrl(img,response.url)
            imageDict[url] = {"id":ArticleUtils.getArticleId(url),"contentUrl":img,"url":url}
        return imageDict

    @classmethod
    def getContentImages4RegexContent(cls, regexContent, response):
        regexContent = regexContent + "//img//@src"
        images = response.xpath(regexContent).extract()
        return images

    @classmethod
    def getContentFiles(cls, response):
        filesRegex = []
        for postfix in ArticleUtils.FILE_POSTFIXS:
            filesRegex.append('contains(@href,"%s")' % postfix)
        postfixR = " or ".join(filesRegex)
        hrefs = response.xpath('//a[(' + postfixR + ') and text()]').extract()
        links = response.xpath('//a[(' + postfixR + ') and text()]//@href').extract()
        # names = response.xpath('//a[' + postfixR + ']//text()').extract()
        if len(links) <= 0:
            return None
        linkDict = {}
        nameDict = {}
        for i, link in enumerate(links):
            if not ArticleUtils.isFile(link):
                continue
            linkDict[link] = ArticleUtils.getFullUrl(link, response.url)
            if i < len(hrefs):
                name = ArticleUtils.removeAllTag(hrefs[i])
                nameDict[link] = name
        fileDict = {}
        for (k, v) in linkDict.items():
            contentFileName = ""
            if k in nameDict:
                contentFileName = nameDict[k]
            fileInfo = {"id": ArticleUtils.getArticleId(v), "name": contentFileName, "contentUrl": k, "url": v}
            fileDict[v] = fileInfo
        return fileDict



    @classmethod
    def isFile(cls, fileName):
        if StringUtils.isEmpty(fileName):
            return False
        if ArticleUtils.FILE_PATTERN.match(fileName.lower()) is not None:
            return True
        return False

    @classmethod
    def isErrorTitle(cls, title):
        if StringUtils.isEmpty(title):
            return False
        if ArticleUtils.ERROR_PAGE_PATTERN.match(title) is not None:
            return True
        if ArticleUtils.ERROR_PAGE_TITLE_PATTERN.match(title) is not None and len(title)<10:
            return True
        return False

    @classmethod
    def isErrorContent(cls,content):
        contentRemoveTag = StringUtils.trim(ArticleUtils.removeAllTag(content))
        contentRemoveTag = contentRemoveTag.replace(" ","")
        if ArticleUtils.ERROR_PAGE_CONTENT_PATTERN.match(contentRemoveTag) is not None and len(contentRemoveTag) < 1000:
            return True
        return False

    @classmethod
    def meta2item(cls, meta,url):
        seed = meta["seedInfo"]
        referer = seed.url
        item = CrawlResultItem()
        item["mediaFrom"] = seed.mediaFrom
        item["referer"] = referer
        item["url"] = url
        item["site"] = seed.site
        listData = {}
        if "listData" in meta:
            listData = meta["listData"]
        item["parse"] =  "detail"
        item["category"] = seed.category
        item["urlLabel"] = seed.urlLabel.split(",")
        item["crawlName"] = seed.crawlName
        item["crawlId"] = str(seed.crawlId)
        item["timestamp"] = meta["timestamp"]
        if StringUtils.isNotEmpty(seed.organization):
            item["organization"] = seed.organization
        for (k, v) in listData.items():
            if "category" == k:
                categoryList = []
                if StringUtils.isNotEmpty(seed.category):
                    categoryList.append(seed.category)
                categoryList.append(v)
                item[k] = "/".join(categoryList)
            else:
                item[k] = v
        return item

    # @classmethod
    # def getNextPageUrl(cls,regexs,response):
    #     nextRegexs = regexs
    #     if nextRegexs is None or len(nextRegexs) <= 0:
    #         nextRegexs = ArticleUtils.COMMON_NEXT_PAGE_REGEX
    #     resultFilterRegex = nextRegexs[-1].resultFilterRegex
    #     nextUrls = ArticleUtils.getResponseContents4WebRegex(nextRegexs, response)
    #     targetNextUrls = []
    #     if nextUrls is not None and len(nextUrls) > 0:
    #         for nextUrl in nextUrls:
    #             if StringUtils.isEmpty(nextUrl):
    #                 continue
    #             if "javascript:" in nextUrl:
    #                 continue
    #             nextUrlTmp = nextUrl.replace('"',"")
    #             nextUrlTmp = nextUrlTmp.replace("'","")
    #             if StringUtils.isEmpty(nextUrlTmp):
    #                 continue
    #             if StringUtils.isNotEmpty(resultFilterRegex) and not re.match(resultFilterRegex, nextUrlTmp):
    #                 continue
    #             targetUrl = ArticleUtils.getFullUrl(nextUrlTmp,response.url)
    #
    #             targetNextUrls.append(targetUrl)
    #     return targetNextUrls

    @classmethod
    def cleanPageUrl(cls, nextUrls, resultFilterRegex, response):
        '''
        原本getNextPageUrl中的方法，对urls进行清洗
        '''
        targetNextUrls = []
        if nextUrls is not None and len(nextUrls) > 0:
            for nextUrl in nextUrls:
                if StringUtils.isEmpty(nextUrl):
                    continue
                if "javascript:" in nextUrl:
                    continue
                nextUrlTmp = nextUrl.replace('"', "")
                nextUrlTmp = nextUrlTmp.replace("'", "")
                if StringUtils.isEmpty(nextUrlTmp):
                    continue
                if StringUtils.isNotEmpty(resultFilterRegex) and not re.match(resultFilterRegex, nextUrlTmp):
                    continue
                targetUrl = ArticleUtils.getFullUrl(nextUrlTmp, response.url)
                targetNextUrls.append(targetUrl)
        return targetNextUrls

    @classmethod
    def getNextPageUrl(cls, regexs, response, currentPage):
        '''
        返回下页url
        @currentPage： 当前页号
        @isList: Ture：识别列表页 False:识别详情页
        '''
        nextRegexs = regexs
        if nextRegexs is None or len(nextRegexs) <= 0:
            nextRegexs = ArticleUtils.COMMON_NEXT_PAGE_REGEX
        resultFilterRegex = nextRegexs[-1].resultFilterRegex
        nextUrls = ArticleUtils.getResponseContents4WebRegex(nextRegexs, response)
        # print(nextUrls)
        targetNextUrls = ArticleUtils.cleanPageUrl(nextUrls, resultFilterRegex, response)
        # print(targetNextUrls)
        if targetNextUrls == [] and currentPage is not None:
            # print("a[contains(text(),'%d页') or text()='%d']//@href"%(currentPage+1,currentPage+1))
            nextUrls = response.xpath(
                "//a[contains(text(),'%d页') or text()='%d']//@href" % (currentPage + 1, currentPage + 1)).extract()
            targetNextUrls = ArticleUtils.cleanPageUrl(nextUrls, resultFilterRegex, response)
        return targetNextUrls

    @classmethod
    def mergeDict(cls, detailDict, field,fieldValue):
        if field is None or fieldValue is None:
            return
        if field not in detailDict:
            detailDict[field] = fieldValue
        elif field in ArticleUtils.MERGE_FIELD:
            if "contentImages" == field or "contentFiles" == field:
                detailFiles = detailDict[field]
                for (k,v) in fieldValue.items():
                    detailFiles[k] = v
                detailDict[field] = detailFiles
            else:
                detailValue = detailDict[field]
                detailValue = detailValue + fieldValue
                detailDict[field] = detailValue

    @classmethod
    def mergeNewDict(cls, detailDict, newDetailDict):
        if newDetailDict is None:
            return
        for (k,v) in newDetailDict.items():
            ArticleUtils.mergeDict(detailDict,k,v)

    @classmethod
    def getDownloadFile(cls,urls,publishAt):
        result = []
        for url in urls:
           result.append({"url":url,"publishAt":publishAt})
        return result

    @classmethod
    def isRender(cls, meta,spiderName):
        if "renderType" in meta and meta["renderType"] == 1:
            return True
        if spiderName.startswith("history_") and "pageRenderType" in meta and meta["pageRenderType"] == 1:
            return True
        return False

    @classmethod
    def getAutoDetail(cls, contentPageNumber,html, enableDownloadImage=False, enableSnapshot=False):
        autoDetail = {}
        try:

            doc = Document(html)
            # response.
            if contentPageNumber<=1:
                autoDetail["title"] = ArticleUtils.cleanHeadTitle(doc.title())
                # autoDetail["publishAt"] = TimeUtils.get_conent_time(html)
                # autoDetail["html"] = html
            contentSnapshot = doc.summary()
            if StringUtils.isNotEmpty(ArticleUtils.removeAllTag(contentSnapshot)):
                if enableSnapshot:
                    autoDetail["contentSnapshot"] = contentSnapshot.replace("<html>", "").replace("</html>","").replace("<body>","").replace("</body>", "")
                autoDetail["content"] = ArticleUtils.removeTag4Content(contentSnapshot)
                if enableDownloadImage:
                    autoDetail["contentImages"] = ArticleUtils.get_content_image_urls(contentSnapshot, response.url)
        except Exception as e:
            return autoDetail
        return autoDetail

    @classmethod
    def get_content_image_urls(cls, html, source_url):
        '''
        @param html:正文html
        @param url:本站地址
        @return ：图片字典dict
        '''
        replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
        img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式
        img_url_list = []
        need_replace_list = re.findall(replace_pattern, html)  # 找到所有的img标签
        for tag in need_replace_list:
            url = re.findall(img_url_pattern, tag)
            if url != []:
                img_url_list.append(url[0])  # 找到所有的img_url
        imageDict = {}
        for img in img_url_list:
            if StringUtils.isEmpty(img):
                continue
            if img.startswith("data:"):
                continue
            # 图片以二进制格式写在网页,不需要下载
            url = ArticleUtils.getFullUrl(img, source_url)
            imageDict[url] = {"id": ArticleUtils.getArticleId(url), "contentUrl": img, "url": url}
        return imageDict

    @classmethod
    def isErrorPage(cls, detail):
        if ArticleUtils.isFile(detail["url"]):
            return False
        if "content" not in detail:
            return True
        contentRemoveTag = ArticleUtils.removeAllTag(detail["content"])
        if StringUtils.isEmpty(contentRemoveTag) and ("contentImages" not in detail or StringUtils.isEmpty(detail["contentImages"])) and ("contentFiles" not in detail or StringUtils.isEmpty(detail["contentFiles"])):
            return True
        if "headTitle" in detail:
            headTitle = detail["headTitle"]
            if ArticleUtils.isErrorTitle(headTitle):
                return True
        if "title" not in detail:
            return True
        title = detail["title"]
        if ArticleUtils.isErrorTitle(title):
            return True
        if ArticleUtils.isErrorContent(detail["content"]):
            return True
        return False

    @classmethod
    def isHistory(cls, spiderName):
        return spiderName.startswith("history_")

    @classmethod
    def isStat(cls, spiderName):
        return "auto_" not in spiderName and "test_" not in spiderName and not ArticleUtils.isHistory(spiderName)

    @classmethod
    def isNotTest(cls, spiderName):
        return "test_" not in spiderName

    @classmethod
    def cleanHeadTitle(cls, headTitle):
        if "_" in headTitle and len(StringUtils.trim(headTitle.split("_")[0])) >= 5:
            return StringUtils.trim(ArticleUtils.removeAllTag(headTitle.split("_")[0]))
        if "--" in headTitle and len(StringUtils.trim(headTitle.split("--")[0])) >=5:
            return StringUtils.trim(ArticleUtils.removeAllTag(headTitle.split("--")[0]))
        return StringUtils.trim(ArticleUtils.removeAllTag(headTitle))

    @classmethod
    def isErrorUrl(cls, url):
        if url is None:
            return True
        if ArticleUtils.ERROR_URL_PATTERN.match(url) is not None:
            return False
        return True
