from crawl_commons.utils.http_util import *
from crawl_commons.utils.string_util import *
from crawl_commons.utils.article_util import *
from crawl_commons.utils.annotation import *
from scrapy.utils.project import get_project_settings
import logging

@singleton
class FileDownloadRepository:
    def __init__(self):
        settings = get_project_settings()
        self.logger = logging.getLogger("fileDownloadRepository")
        # self.url = 'http://file-download-service:31001/download?urls=%s&publishAt=%s'
        self.url = settings.get("FILE_DOWNLOAD_URL")
        self.logger.info("init download url %s" % self.url)


    def download(self,urls,publishAt):
        downloads = ArticleUtils.getDownloadFile(urls,publishAt)
        self.logger.info("download %s" % downloads)
        result = HttpUtils.postJsonQuery(self.url,downloads)
        self.logger.info("download result %s" % (result))