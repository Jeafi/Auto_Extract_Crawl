# -*- coding: utf-8 -*-
import json
from crawl_commons.utils.http_util import *
from scrapy.utils.project import get_project_settings
from scrapy.utils.conf import get_config

class StringUtils(object):

    @classmethod
    def trim(cls,str):
        if str is None:
            return ""
        str = str.strip()
        return str

    @classmethod
    def isEmpty(cls, str):
        if str is None or len(StringUtils.trim(str))<=0:
            return True
        return False

    @classmethod
    def isNotEmpty(cls, str):
        return not StringUtils.isEmpty(str)

    @classmethod
    def dict2Json(cls, dictData):
        encode_json = json.dumps(dictData,ensure_ascii=False)
        return encode_json

    @classmethod
    def replaceSpecialWords(cls, str):
        if str is None:
            return ""
        dd = str.replace('\n', ' ')
        dd = dd.replace('\t', ' ')
        dd = dd.replace('\r', ' ')
        dd = dd.replace('\r\n', ' ')
        dd = dd.replace(u'\xa0', ' ')
        dd = dd.replace(u'\u3000', ' ')
        dd = dd.replace(u'\u2002',' ')
        return dd

    @classmethod
    def getCrawlInfoAddress(cls):
        settings = get_project_settings()
        localIp = settings.get("CRAWL_IP", HttpUtils.get_ip_address())
        cfg = get_config()
        scrapydUrl = cfg.get('deploy', "url").replace("http://", "").replace("/", "")
        address = scrapydUrl.replace("localhost", localIp)
        return address