# Scrapy settings for PoemScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "PoemScrapy"

SPIDER_MODULES = ["PoemScrapy.spiders"]
NEWSPIDER_MODULE = "PoemScrapy.spiders"

ADDONS = {}

# 分布式核心设置
# 启用Redis调度器（替代默认的本地调度器）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 启用Redis去重器（替代默认的RFPDupefilter)
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度器持久化:爬虫关闭时保留Redis中的队列和去重数据
SCHEDULER_PERSIST = True

#　Redis连接配置 格式：redis://:密码@主机：端口/数据库编号
REDIS_URl = "redis://localhost:6379/0"
# 方式二
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379
# REDIS_PASSWORD = "" # 如果有
# REDIS_DB = 0

# 可选配置
#　使用优先级队列（默认是SpiderQueue,先进先出）
# 不同队列类型：SpiderQueue（插入顺序），SpiderStack（出入逆序），priorityQueue(优先级分数)
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"

# 每次从Redis批量获取的请求数量
REDIS_START_URLS_BATCH_SIZE = 16




# Crawl responsibly by identifying yourself (and your website) on the user-agent
'''通过在用户代理中标识自己（及您的网站）来负责任地爬取
'''
USER_AGENT = 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
'''并发和限流设置'''
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 2 # 每个域名的并发请求数
DOWNLOAD_DELAY = 1 # 下载延迟
# 随机下载延迟（0.5-1.5倍DOWNLOAD_DELAY）
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default) #启用和禁用cookie
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
'''禁用 Telnet 控制台（默认启用）
'''
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
'''覆盖默认请求头'''
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "PoemScrapy.middlewares.PoemscrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "PoemScrapy.middlewares.PoemscrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "PoemScrapy.pipelines.PoemscrapyPipeline": 300,
   # 启用Redis Pipeline，将Item存入Redis
   "scrapy_redis.pipelines.RedisPipeline": 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
'''启用并配置 AutoThrottle 扩展（默认情况下已禁用）
'''
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
