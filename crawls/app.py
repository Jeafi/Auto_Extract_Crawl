

from crawl_commons.utils.http_util import *
from crawl_commons.utils.string_util import *
from scrapy.utils.project import get_project_settings
from scrapy.utils.conf import get_config
import time
import schedule
import datetime
# import logging
# import sys

# logger = None

def runSpider(url,projectName,spiderName):
    query={'project':projectName,'spider':spiderName}
    # logger.info("start run %s %s %s" %(url,projectName,spiderName))
    now = datetime.datetime.now()
    print("%s start run %s %s %s" %(now,url,projectName,spiderName))
    # sys.stderr.write("%s start run %s %s %s" %(now,url,projectName,spiderName))
    requestUrl = url+"schedule.json"
    result = HttpUtils.postQuery(requestUrl,query)
    # logger.info(result)
    now = datetime.datetime.now()
    print("%s %s" % (now,result))
    # sys.stderr.write("%s %s" % (now,result))


def getCrawlInfo():
    settings = get_project_settings()
    address = StringUtils.getCrawlInfoAddress()
    url = settings.get("CRAWL_INFO_SCHEDULE_URL") % (address,"","")
    jsonResult = HttpUtils.getUrl(url)
    list = jsonResult["data"]
    return list


def test(url, project):
    print("%s %s" % (url,project))
    # logger.info("%s %s" % (url,project))

if __name__ == '__main__':
    # logging.basicConfig(filename="/home/yhye/python_project/gemantic-python/crawl_selected/log.conf")
    # logger = logging.getLogger("main")
    cfg = get_config()
    url = cfg.get('deploy', "url")
    settings = get_project_settings()
    # project = settings.get("BOT_NAME")

    # logger.info("start schedule %s %s" % (url,project))
    now = datetime.datetime.now()
    # sys.stderr.write("%s start schedule %s %s" % (now,url, project))
    print("%s start schedule %s" % (now,url))
    # schedule.every().minute.do(test,url,project)
    crawlInfos = getCrawlInfo()
    print(crawlInfos)
    for crawlInfo in crawlInfos:
        scheduleType = crawlInfo["scheduleType"]
        scheduleEvery = crawlInfo["schedule"]
        project = crawlInfo["project"]
        crawlName = crawlInfo["crawlName"]
        if "HOUR" == scheduleType:
            if "1" == scheduleEvery:
                schedule.every().hour.do(runSpider, url, project,crawlName)
            else:
                schedule.every(int(scheduleEvery)).hours.do(runSpider, url, project,crawlName)
        elif "MINUTE" == scheduleType:
            if "1" == scheduleEvery:
                schedule.every().minute.do(runSpider, url, project,crawlName)
            else:
                schedule.every(int(scheduleEvery)).minute.do(runSpider, url, project,crawlName)
    while True:
        schedule.run_pending()
        time.sleep(1)
