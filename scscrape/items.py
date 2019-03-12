# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class YearItem(scrapy.Item):
    # define the fields for your item here like:
    info = scrapy.Field()
    round_array = scrapy.Field()
    date_array = scrapy.Field()
    opponent_array = scrapy.Field()
    result_array = scrapy.Field()
    AFscore_array = scrapy.Field()
    SCscore_array = scrapy.Field() # round/date/opponent/score/AF/SC
    pass

class PlayerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    info_team = scrapy.Field()
    info1 = scrapy.Field()
    info2 = scrapy.Field()
    info_draft = scrapy.Field()
    sc_price = scrapy.Field()

    pass