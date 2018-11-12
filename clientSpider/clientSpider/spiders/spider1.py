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
        self.seleniumUtils.loginManual('https://www.tianyancha.com/')
        self.start_urls = ScrapyUtils.init("http://www.hbggzy.cn/jydt/003001/003001005/%s.html", 2)

    # endregion

    # region parse

    def parse(self, oResponse):
        oSelector = ScrapyUtils.getSelector(oResponse)
        arrDomArticle = ScrapyUtils.xpath('//ul[@class="ewb-news-items"]/li', oSelector)
        for oDomArticle in arrDomArticle:
            oItem = SpiderItem()
            oItem['url'] = 'http://www.hbggzy.cn' + ScrapyUtils.xpath2('a/@href', oDomArticle, False)
            oItem['title'] = ScrapyUtils.xpath2('a/@title', oDomArticle, True)

            oRequest = ScrapyUtils.postWithItem(oItem['url'], oItem, self._parseRecursive)
            yield oRequest

    def _parseRecursive(self, oResponse):
        oSelector = Selector(oResponse)
        oItem = oResponse.meta['item']
        oDomClientCompany = ScrapyUtils.xpath('//div[@class="news-article-para"]/table/tr[9]/td[2]/div/text()',
                                              oSelector)
        oItem["clientCompany"] = ScrapyUtils.extract(oDomClientCompany, True)
        oDomClientPrice = ScrapyUtils.xpath('//div[@class="news-article-para"]/table/tr[9]/td[3]/div/text()', oSelector)
        oItem["clientPrice"] = ScrapyUtils.extract(oDomClientPrice, True)
        oDomClientDesc = ScrapyUtils.xpath('//div[@class="news-article-para"]/table/tr[9]/td[4]/div/text()', oSelector)
        oItem["clientDesc"] = ScrapyUtils.extract(oDomClientDesc, True)
        oItem["clientPhone"] = self._parsePhone(oItem["clientCompany"])
        yield oItem

    def _parsePhone(self, strQuery):
        try:
            # get strPreText
            self.seleniumUtils.get('https://www.tianyancha.com/search/suggest.json?key=' + strQuery)
            strPreText = self.seleniumUtils.getEleByTag("pre").text

            # get oJson
            oJson = JsonUtils.get(strPreText)

            # get strId
            strId = ""
            for oJsonItem in oJson:
                strCompanyName = oJsonItem.get("name").replace("<em>", "").replace("</em>", "")
                if strCompanyName == strQuery:
                    strId = oJsonItem.get("id")
                    break
            # if strId is empty
            if strId == "":
                strPhone = strId
            # if strId is not empty
            else:
                strPhone = self._parsePhoneDetails(strQuery, strId)
            return strPhone
        except Exception as e:
            print(str(e))
            return ""

    def _parsePhoneDetails(self, strQuery, strId):
        self.seleniumUtils.get('https://www.tianyancha.com/company/' + str(strId))
        strPhone = self.seleniumUtils.getEleByXPath("./*//div[@class='detail ']/*//div[@class='in-block']/span[2]").text
        strRes = "{0},{1}\n".format(strQuery, strPhone)
        return strRes

    # endregion


# TODO:移到core-fw-python
class SeleniumUtils:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def loginManual(self, strUrl):
        print("启动浏览器，打开天眼查登录界面")
        self.driver.get(strUrl)
        print("手动登录，等待60s......")
        time.sleep(60)
        print("登录成功")
        self.driver.get(strUrl)

    def get(self, strUrl):
        self.driver.get(strUrl)

    def getEleByTag(self, strTagName):
        oEle = self.driver.find_element_by_tag_name(strTagName)
        return oEle

    def getEleByXPath(self, strXPath):
        oEle = self.driver.find_element_by_xpath(strXPath)
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
    def xpath(strXPath, oSelector):
        return oSelector.xpath(strXPath)

    @staticmethod
    def xpath2(strXPath, oDom, bEncode):
        if bEncode:
            return oDom.xpath(strXPath).extract()[0].encode('utf-8')
        else:
            return oDom.xpath(strXPath).extract()[0]

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
