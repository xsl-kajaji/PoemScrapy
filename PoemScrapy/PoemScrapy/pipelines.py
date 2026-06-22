# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from encodings.punycode import selective_find
import csv

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from scrapy import crawler
import pymysql

class PoemscrapyPipeline:

    def __init__(self):
        self.file_name = 'poem.csv'
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        '''例如打开数据库'''
        # 爬虫启动时创建数据库链接
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1913',
            db='company',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('drop table if exists items')
        # 创建表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS items(
            sentence varchar(100) unique not null,
            source varchar(100),
            href varchar(100)
            )''')
        self.conn.commit()

        # 写入文件
        self.file = open(self.file_name,mode='w',newline="",encoding='utf-8-sig')
        self.writer = csv.DictWriter(self.file,fieldnames=['sentence','source','href'])
        self.writer.writeheader()

    def process_item(self, item, spider):
        '''例如处理数据并插入数据库'''
        self.cursor.execute('''
        INSERT INTO items(sentence, source, href)
        values(%s,%s,%s)''',(item['sentence'],item['source'],item['href']))
        self.conn.commit()
        # self.cursor.execute("select sentence,source,href from items")
        # print(self.cursor.fetchall())

        self.writer.writerow(item)

        return item

    def close_spider(self, spider):
        '''例如关闭数据'''
        self.cursor.execute("select sentence,source,href from items")
        print(self.cursor.fetchall())
        self.conn.close()

        if self.file:
            self.file.close()


'''异步MySQL数据库'''
# import aiomysql
# import logging
#
#
# class AsyncMysqlPipeline:
#     """
#     异步 MySQL 数据管道
#     支持：连接池、异步插入、异常处理、自动重连
#     """
#
#     def __init__(self):
#         # 数据库配置
#         self.db_config = {
#             'host': 'localhost',
#             'port': 3306,
#             'user': 'root',
#             'password': '你的密码',
#             'db': 'company',  # 数据库名
#             'charset': 'utf8mb4',
#             'autocommit': True
#         }
#
#         self.pool = None  # 异步连接池
#         self.logger = logging.getLogger(__name__)
#
#     async def open_spider(self, spider):
#         """
#         爬虫启动时：创建异步连接池
#         """
#         try:
#             self.pool = await aiomysql.create_pool(**self.db_config)
#             self.logger.info("✅ 异步 MySQL 连接池创建成功")
#         except Exception as e:
#             self.logger.error(f"❌ 数据库连接失败: {e}")
#
#     async def close_spider(self, spider):
#         """
#         爬虫关闭时：关闭连接池
#         """
#         if self.pool:
#             self.pool.close()
#             await self.pool.wait_closed()
#             self.logger.info("✅ 异步 MySQL 连接池已关闭")
#
#     async def process_item(self, item, spider):
#         """
#         异步处理数据（核心）
#         """
#         if not self.pool:
#             self.logger.error("❌ 数据库连接未初始化")
#             return item
#
#         try:
#             # 从连接池获取连接
#             async with self.pool.acquire() as conn:
#                 async with conn.cursor() as cursor:
#                     # 编写 SQL（根据你的 Item 修改）
#                     sql = """
#                     INSERT INTO items (sentence, source, href)
#                     VALUES (%s, %s, %s)
#                     """
#
#                     # 数据
#                     args = (
#                         item.get('sentence', ''),
#                         item.get('source', ''),
#                         item.get('href', '')
#                     )
#
#                     # 异步执行
#                     await cursor.execute(sql, args)
#
#             self.logger.info(f"✅ 成功写入: {item.get('sentence')}")
#
#         except Exception as e:
#             self.logger.error(f"❌ 数据写入失败: {e} | Item: {item}")
#
#         return item