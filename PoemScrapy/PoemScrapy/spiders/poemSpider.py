
import scrapy
from ..items import PoemscrapyItem
from scrapy_redis.spiders import RedisSpider
import ujson

class PoemspiderSpider(RedisSpider):
    name = "poemSpider" #区别不同爬虫
    allowed_domains = ["guwendao.net"] #允许访问的域
    # start_urls = ["http://guwendao.net/mingjus/"]
    data = {"name":"xinYi","age":"17"}
    redis_key = "poemSpider:start_urls" # Redis中存储种子URL的键名

    # 可在此方法下对要请求的页面进行处理,定义请求参数
    # def start_requests(self):
    #     # 进行post请求,两种方法
    #     yield scrapy.http.FormRequest(self.start_urls[0],callback=self.parse(),formdata=self.data)
    #     yield scrapy.http.JsonRequest(self.start_urls[0],callback=self.parse(),formdata=self.data)


    def parse(self, response, **kwargs):

        # 返回内容字符串
        # response.text
        # 返回内容二进制
        # response.body

        print(response.status)
        # xpath
        # contents = response.css('div.left div.cont')
        # for content in contents:
        #     item = PoemscrapyItem()
        #     item['sentence'] = response.xpath('//div[@class="left"]//div[@class="cont"]/a[1]/text()').getall()
        #     item['source'] = response.xpath('//div[@class="left"]//div[@class="cont"]/a[2]/text()').getall()
        #     item['href'] = response.xpath('//div[@class="left"]//div[@class="cont"]/a[1]/@href').getall()
        #     yield item

        # css
        contents = response.css('div.left div.cont')
        for content in contents:
            # 生成数据对象
            item = PoemscrapyItem()
            item['sentence'] = content.css('a:nth-of-type(1)::text').get().strip() if content.css('a:nth-of-type(1)::text') else ''
            item['source'] = content.css('a:nth-of-type(2)::text').get().strip() if content.css('a:nth-of-type(2)::text') else ''
            item['href'] = content.css('a:nth-of-type(1)::attr(href)').get().strip() if content.css('a:nth-of-type(1)::text') else ''
            # 返回数据
            yield item

        next_page = response.css('a.amore ::attr(href)').get()
        print(next_page)
        # next_url = response.urljoin(next_page)
        # print(next_url)
        # 爬取下一页
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
        # yield scrapy.Request(next_url,callback=self.parse)


'''处理动态网页的两种方法，直接查看API和selenium'''
# import scrapy
# import json
#
#
# class APISpider(scrapy.Spider):
#     name = 'api'
#     start_urls = ['https://api.example.com/data?page=1']
#
#     def parse(self, response):
#         data = json.loads(response.text)
#         for item in data['results']:
#             yield {
#                 'title': item['title'],
#                 'content': item['content']
#             }
#
#         # 处理下一页
#         next_page = data['next']
#         if next_page:
#             yield scrapy.Request(next_page, callback=self.parse)
#
#
# import scrapy
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
#
# class SeleniumSpider(scrapy.Spider):
#     name = 'selenium'
#     start_urls = ['https://example.com/dynamic-page']
#
#     def __init__(self):
#         # 配置Chrome无头模式
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         self.driver = webdriver.Chrome(options=chrome_options)
#
#     def parse(self, response):
#         # 使用Selenium加载页面
#         self.driver.get(response.url)
#         # 等待页面加载完成
#         self.driver.implicitly_wait(10)
#
#         # 获取渲染后的HTML
#         html = self.driver.page_source
#         # 创建新的响应对象
#         response = scrapy.http.HtmlResponse(
#             url=self.driver.current_url,
#             body=html,
#             encoding='utf-8'
#         )
#
#         # 解析数据
#         items = response.css('div.item')
#         for item in items:
#             yield {
#                 'title': item.css('h3::text').get()
#             }
#
#     def closed(self, reason):
#         # 关闭浏览器
#         self.driver.quit()
#
