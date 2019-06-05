from crawl_commons.repository.seed import *
from crawl_commons.repository.filedownload import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.time_util import *
from crawl_commons.utils.http_util import *
import copy
import json
import sys
print(sys.path)
print(sys.modules.keys())
# seedRepositroy = SeedRepository()
# crawlRegexDict = seedRepositroy.get_regex("http://finance.sina.com.cn/zl/")
# for i,v in enumerate(crawlRegexDict):
#     print(i)
#     print(v.depthNumber)
#     for (k2,v2) in v.regexDict.items():
#         print(k2)
#         print("@@")
#         for r in v2:
#             print(r)
#             print("**")
#     # for (k2, v2) in v.regexDict:
#     #     print(k2)
#     print("-----------------------------")
# dict = {}
# dict[1] = "aa"
# dict[2] = "bb"
# dict1 = dict.copy()
# dict1[1] = "aa1"
# dict1[3] = "cc"
# print(dict)
# print(dict1)
#
# list = []
# list.append("a")
# list.append("b")
# print(list[0])

# url = ArticleUtils.getFullUrl("http://sousuo.gov.cn/list.htm?q=&n=15&p=1&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime=","http://sousuo.gov.cn/list.htm?q=&n=15&p=0&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime=")
#
# print(url)

file = "sdfaf.doc"
# dr = re.compile(u'.*?\.(pdf|doc|xls|xlsx|docx|pptx|ppt|)$')
# result = dr.match(file)
# print(result)
# print(ArticleUtils.isFile(file))
#
# regex = WebRegex({"regexType":"xpath","renderType":"0","maxPageNumber":"0","regexField":"nextPage", "regexContent":'//div[@id="UCAP-CONTENT"]//p|//td[@id="UCAP-CONTENT"]//p',"resultFormat":"","renderBrowser":"","regexSort":"0","depthNumber" :"0","resultFilterRegex":""})
# regexCopy = copy.copy(regex)
# imageRegexs = regexCopy.regexContent.split("|")
# rc = "//img//@src|".join(imageRegexs)+"//img//@src"
# regexCopy.setRegexContent("contentImages",rc)
# print(regexCopy)
# print(regex)
# id = ArticleUtils.getArticleId("http://www.gov.cn/xinwen/2018-11/21/content_5342200.htm")
# print(id)
# print(isinstance(rc,str))
#
# dict = {}
# dict["5339622/images/5255deb4ce9f43398f1f71d93124402e.jpg"]=2
# print(dict)
# dict["contentFiles"] = {"1.jpg":{"contentUrl":"1.jpg","url":"http://sdfs/1.jpg"}}
# dict["content"] = "正文测试"
# ArticleUtils.mergeDict(dict,"dsf",123)
# ArticleUtils.mergeDict(dict,"contentFiles",{"2.jpg":{"contentUrl":"2.jpg","url":"http://sdfs/2.jpg"}})
# ArticleUtils.mergeDict(dict,"content","二段正文测试")
# print(dict)

# repository = FileDownloadRepository()
# repository.download(["https://www.baidu.com/img/bd_logo1.png"],TimeUtils.getNowMill())
# print(ArticleUtils.getFullUrl("?3","http://www.mofcom.gov.cn/article/ae/ag/?2"))
# print('//div[@id="zoom"]//p|//div[@id="zoom"]//div|//div[@class="txt1"]//div|//div[@class="txt1"]//text()'.split("|"))
# content = 'safsdfsaf<script type="text/javascript">function videoChange(){	$("playbtn_img").css({"left":((document.documentElement.clientWidth-20)-70)/2+"px","top":(300-70)/2+"px"});	$("#video_content_is_loading").css({"left":((document.documentElement.clientWidth-20)-120)/2+"px","top":(300-120)/2+"px"});}$(window).resize(function(){ videoChange();})function isAppendSpace(i){console.log(i);$("#playbtn_img").length>0? videoChange() : "";i-- && i>=0 && $("#playbtn_img").length == 0 ? setTimeout(function(){isAppendSpace(i)},500) : "";}isAppendSpace(5);</script>'
# print(ArticleUtils.removeTag4Content(content))

content2 = 'sfda<p align="center"><font color="#0000cc">图表6：2005年度部分国家军人人均国防费（金额单位：千美元） 新华社发<p align="center"><a href="307878.htm">1</a>  <a href="307878_1.htm">2</a>  <a href="307878_2.htm">3</a>  <a href="307878_3.htm">4</a>  <a href="307878_4.htm">5</a>  <a href="307878_5.htm">6</a>  <a href="307878_6.htm">7</a>  <a href="307878_7.htm">8</a>  <a href="307878_8.htm">9</a>  <a href="307878_9.htm">10</a>  <a href="307878.htm">首页</a>  <a href="307878_7.htm">上页</a>  <a href="307878_9.htm">下页</a>  <a href="307878_9.htm">末页</a></p>  </font></p>'
# <div [^>]*id='footer'[^>]*>(<div[^>]*>(<div[^>]*>.*?</div>|.)*?</div>|.)*?</div>
dr = re.compile(u'<p.*?>.*?(<p.*?>.*?(>上页</|>上一页</|>下页</|>下一页</).*?</p>).*?</p>',re.S)
content2 = dr.sub(u"", content2)
print(content2)

print(ArticleUtils.getArticleId("http://www.mofcom.gov.cn/article/zhengcejd/bq/200407/20040700250926.shtml"))

print(HttpUtils.get_ip_address())
#print(re.match(".*?\?\d+","http://www.mofcom.gov.cn/article/ae/ag/2"))
# filesRegex = []
# for postfix in ArticleUtils.FILE_POSTFIXS:
#     filesRegex.append('contains(@href,"%s")' % postfix)
# postfixR = " or ".join(filesRegex)
# print(postfixR)
# print("//a["+postfixR+"]//@href")
# print(ArticleUtils.isFile("./P020181128377923136457.pdf"))

# json='[{ "_id" : "447d4887841e1f8dbf73417cfc11be5c", "url" : "http://www.mofcom.gov.cn/contentimage/Jun6,2012104353AM.jpg", "contentUrl" : "http://www.mofcom.gov.cn/contentimage/Jun6,2012104353AM.jpg" }]'
# print(json.loads(json))

# print(ArticleUtils.getFullUrl("article/30423121","http://jhsjk.people.cn/result?form=701&else=501"))
#
# print(len("2015-03-03"))