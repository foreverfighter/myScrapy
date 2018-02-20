# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwilightstrategyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    side = scrapy.Field()
    ops = scrapy.Field()
    removed = scrapy.Field()
    timestamp = scrapy.Field()
    failmsg = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
