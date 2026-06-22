# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 自定义去重逻辑
# 默认的去重过滤器灰根据URL、请求方法和请求体生成指纹。
# 如果需要忽略某些参数，可以自定一指纹生成逻辑
import re
import hashlib
import json
from scrapy.utils.python import to_unicode
from scrapy_redis.dupefilter import RFPDupeFilter
class TestRFPDupeFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        # 移除URL的时间戳参数
        url = re.sub(r'timestamp=\d+','',request.url)
        # 标准化URL
        from w3lib.url import canonicalize_url
        url = canonicalize_url(url)

        fingerprint_data = {
            "method": to_unicode(request.method),
            "url": url,
            "body": (request.body or b"").hex()
        }
        fingerprint_json = json.dumps(fingerprint_data,sort_keys=True)
        return hashlib.sha1(fingerprint_json.encode()).hexdigest()
    # 启用：DUPEFILTER_CLASS = "PoemSpider.middlewares.TestRFPDupeFilter"

class PoemscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        '''对于每个经过爬虫中间件并进入爬虫的响应都会被调用'''
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        '''在Spider返回结果并处理响应之后调用'''
        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class PoemscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        '''为每个通过下载器中间件的请求调用
'''
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
