# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class BaimaPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",database="test",user="root",password="123456",port=3306,charset="utf8")
        self.cursor = self.conn .cursor()


    def process_item(self, item, spider):
        sql_value = "insert into books values ('{}','{}','{}','{}',{},{},{})"\
            .format(item['book_name'],item['author'],item['status'],item['type'],item['click'],item['words'],item['ex'])
        self.cursor.execute(
            sql_value
        )
        self.conn.commit()
        return item

    def close(self, spider):
        self.cursor.close()
        self.conn.close()

