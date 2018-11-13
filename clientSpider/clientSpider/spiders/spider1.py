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

    name = "Spdier1"
    allowed_domains = ["hbggzy.cn"]
    start_urls = []

    # endregion

    # region init

    def __init__(self):
        self.seleniumUtils = SeleniumUtils()
        self.seleniumUtils.loginManual('https://www.qichacha.com/', 30)
        self.start_urls = ScrapyUtils.init("http://www.hbggzy.cn/jydt/003001/003001005/%s.html", 20)

    # endregion

    # region parse

    def parse(self, oResponse):
        oSelector = ScrapyUtils.getSelector(oResponse)
        arrDomArticle = ScrapyUtils.findByXPath('//ul[@class="ewb-news-items"]/li', oSelector)
        for oDomArticle in arrDomArticle:
            oItem = SpiderItem()
            # url
            oDomUrl = ScrapyUtils.findByXPath2('a/@href', oDomArticle)
            oItem['url'] = 'http://www.hbggzy.cn' + ScrapyUtils.extract(oDomUrl, False)
            # title
            oDomTitle = ScrapyUtils.findByXPath2('a/@title', oDomArticle)
            oItem['title'] = ScrapyUtils.extract(oDomTitle, True)
            # time
            oDomTime = ScrapyUtils.findByXPath2('span/text()', oDomArticle)
            strTime = ScrapyUtils.extract(oDomTime, True)
            strTime = StrUtils.replace(strTime, '\r\n', '')
            strTime = StrUtils.replace(strTime, '\t', '')
            oItem["time"] = strTime

            oRequest = ScrapyUtils.postWithItem(oItem['url'], oItem, self._parseRecursive)
            yield oRequest

    def _parseRecursive(self, oResponse):
        oSelector = Selector(oResponse)
        oItem = oResponse.meta['item']

        # company
        oDomCompany = ScrapyUtils.findByXPath('//div[@class="news-article-para"]/table/tr[9]/td[2]/div/text()',
                                              oSelector)
        oItem["company"] = ScrapyUtils.extract(oDomCompany, True)
        # price
        oDomPrice = ScrapyUtils.findByXPath('//div[@class="news-article-para"]/table/tr[9]/td[3]/div/text()',
                                            oSelector)
        oItem["price"] = ScrapyUtils.extract(oDomPrice, True)
        # desc
        oDomDesc = ScrapyUtils.findByXPath('//div[@class="news-article-para"]/table/tr[9]/td[4]/div/text()',
                                           oSelector)
        oItem["desc"] = ScrapyUtils.extract(oDomDesc, True)
        oItem["phone"] = self._parsePhone(oItem["company"])
        yield oItem

    def _parsePhone(self, strQuery):
        # oDomCompany
        time.sleep(10)
        self.seleniumUtils.get('https://www.qichacha.com/search?key=' + strQuery)
        oDomCompany = self.seleniumUtils.getEleByClass('ma_h1')
        strCompanyUrl = oDomCompany.get_attribute('href')
        # oDomPhone
        time.sleep(10)
        self.seleniumUtils.get(strCompanyUrl)
        oDomPhone = self.seleniumUtils.getEleByClass('cvlu')
        oDomPhoneA = oDomPhone.find_element_by_tag_name('span')
        strPhone = oDomPhoneA.text
        return strPhone

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
