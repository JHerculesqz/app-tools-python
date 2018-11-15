# coding=utf-8
from selenium import webdriver
import time

import json

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from clientSpider.items import SpiderItem


class Spider1(CrawlSpider):
    # region Fields

    name = "Spdier2"
    allowed_domains = []
    start_urls = []

    # endregion

    # region init

    def __init__(self):
        self.seleniumUtils = SeleniumUtils()
        self.count = 2
        self.start_urls = ['http://www.ccgp-hubei.gov.cn/notice/cggg/pzbgg/index_1.html']

    # endregion

    # region parse

    def parse(self, oResponse):
        #
        self.seleniumUtils.get('http://www.ccgp-hubei.gov.cn/notice/cggg/pzbgg/index_1.html')
        oDomSearch = self.seleniumUtils.getEleById('search')
        #
        oDomFormKey = oDomSearch.find_element_by_name('queryInfo.key')
        oDomFormKey.send_keys(u'软件')
        #
        oDomForm = oDomSearch.find_element_by_id('noticeForm')
        oDomForm.submit()
        #
        arrRes = self._parseItems()
        for oRes in arrRes:
            yield oRes
        #
        for i in range(self.count):
            oDomPage = self.seleniumUtils.getEleByClass('pagination')
            arrDomPageA = oDomPage.find_elements_by_tag_name('a')
            for oDomA in arrDomPageA:
                if oDomA.text == u'下一页':
                    oDomA.click()
                    arrRes = self._parseItems()
                    for oRes in arrRes:
                        yield oRes
                    break

    def _parseItems(self):
        arrRes = []

        oDomRes = self.seleniumUtils.getEleByClass('news-list-content')
        arrDomLi = oDomRes.find_elements_by_tag_name('li')
        for oDomLi in arrDomLi:
            oItem = SpiderItem()
            # a
            oDomA = oDomLi.find_element_by_tag_name('a')
            oItem['url'] = oDomA.get_attribute('href')
            oItem['title'] = oDomA.text
            # span
            oDomSpan = oDomLi.find_element_by_tag_name('span')
            oItem['time'] = oDomSpan.text
            #
            oItem['company'] = ''
            oItem['price'] = ''
            oItem['phone'] = ''
            oItem['desc'] = ''
            arrRes.append(oItem)

        return arrRes

    # endregion


# TODO:移到core-fw-python
class SeleniumUtils:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def loginManual(self, strUrl, iTimeout):
        print('login,wait...')
        self.driver.get(strUrl)
        time.sleep(iTimeout)
        print("login ok...")
        self.driver.get(strUrl)

    def get(self, strUrl):
        self.driver.get(strUrl)

    def getEleByTag(self, strTagName):
        oEle = self.driver.find_element_by_tag_name(strTagName)
        return oEle

    def getEleByXPath(self, strXPath):
        oEle = self.driver.find_element_by_xpath(strXPath)
        return oEle

    def getEleByClass(self, strClassName):
        oEle = self.driver.find_element_by_class_name(strClassName);
        return oEle

    def getEleById(self, strId):
        oEle = self.driver.find_element_by_id(strId);
        return oEle


# TODO:移到core-fw-python
class JsonUtils:
    def __init__(self):
        pass

    @staticmethod
    def get(strUrl):
        oJson = json.loads(strUrl).get("data")
        return oJson


# TODO:移到core-fw-python
class StrUtils:
    def __init__(self):
        pass

    @staticmethod
    def replace(strTarget, strOld, strNew):
        return strTarget.replace(strOld, strNew)


# TODO:移到core-fw-python
class ScrapyUtils:
    def __init__(self):
        pass

    @staticmethod
    def init(strUrlTemplate, iCount):
        arrStartUrls = []
        for i in range(1, iCount):
            arrStartUrls.append(strUrlTemplate % str(i))
        return arrStartUrls

    @staticmethod
    def postWithItem(strUrl, oItem, oCallback):
        oRequest = scrapy.Request(strUrl, oCallback)
        oRequest.meta['item'] = oItem
        return oRequest

    @staticmethod
    def getSelector(oResponse):
        oSelector = Selector(oResponse)
        return oSelector

    @staticmethod
    def findByXPath(strXPath, oSelector):
        return oSelector.xpath(strXPath)

    @staticmethod
    def findByXPath2(strXPath, oDom):
        return oDom.xpath(strXPath)

    @staticmethod
    def extract(oDom, bEncode):
        if bEncode:
            if len(oDom):
                return oDom.extract()[0].encode('utf-8')
            else:
                return ''
        else:
            if len(oDom):
                return oDom.extract()[0]
            else:
                return ''
