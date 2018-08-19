# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoPipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient(spider.settings.get('MONGO_URI'))
        db = client[spider.settings.get('MONGO_DB')]
        table = db[spider.settings.get('MONGO_TABLE')]
        table.update({'name':item['name']},dict(item),True)

