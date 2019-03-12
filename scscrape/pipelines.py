# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""from .items import YearItem, PlayerItem

class FirstPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, YearItem):
            # Save your data here. It's possible to save it to CSV file. Also you can put data to any database you need.
            pass

        return item

class SecondPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PlayerItem):
            # Save your data here. It's possible to save it to CSV file. Also you can put data to any database you need.
            pass

        return item"""


class ScscrapePipeline(object):
    def process_item(self, item, spider):
        return item
