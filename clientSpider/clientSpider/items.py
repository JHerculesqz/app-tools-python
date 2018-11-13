# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SpiderItem(Item):
    url = Field()
    title = Field()
    time = Field()
    company = Field()
    price = Field()
    phone = Field()
    desc = Field()
