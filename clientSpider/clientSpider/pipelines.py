# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook


class ClientspiderPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['url', 'title', 'clientCompany', 'clientPrice', 'clientDesc'])

    def process_item(self, item, spider):
        row = self.ws.max_row + 1
        self.ws.cell(row, 1).value = 'URL'
        self.ws.cell(row, 1).hyperlink = item['url']
        self.ws.cell(row, 2).value = item['title']
        self.ws.cell(row, 3).value = item['clientCompany']
        self.ws.cell(row, 4).value = item['clientPrice']
        self.ws.cell(row, 5).value = item['clientDesc']
        self.wb.save('result.xlsx')
        return item
