from scrapy import cmdline

cmdline.execute("scrapy crawl poemSpider".split())

# # 运行并保存数据到JSON文件
# scrapy crawl quotes -o quotes.json
#
# # 运行并保存数据到CSV文件
# scrapy crawl quotes -o quotes.csv