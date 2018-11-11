# coding=utf-8
import scrapy
import urllib
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from clientSpider.items import SpiderItem


class Spider1(CrawlSpider):
    name = "Spdier1"
    allowed_domains = ["hbggzy.cn"]
    start_urls = []

    def __init__(self):
        # self.start_urls.append("http://www.hbggzy.cn/jydt/003001/003001005/1.html")
        for i in range(50):
            self.start_urls.append("http://www.hbggzy.cn/jydt/003001/003001005/" + str(i) + ".html")

    def parse(self, response):
        selector = Selector(response)
        articles = selector.xpath('//ul[@class="ewb-news-items"]/li')
        for article in articles:
            item = SpiderItem()
            url = article.xpath('a/@href').extract()
            title = article.xpath('a/@title').extract()

            item['url'] = 'http://www.hbggzy.cn' + url[0]
            item['title'] = title[0].encode('utf-8')

            request = scrapy.Request(item['url'], self.subParse)
            request.meta['item'] = item
            yield request

    def subParse(self, response):
        item = response.meta['item']
        selector = Selector(response)
        clientCompanyDiv = selector.xpath('//div[@class="news-article-para"]/table/tr[9]/td[2]/div/text()')
        item["clientCompany"] = clientCompanyDiv.extract()[0].encode('utf-8')
        clientPriceDiv = selector.xpath('//div[@class="news-article-para"]/table/tr[9]/td[3]/div/text()')
        item["clientPrice"] = clientPriceDiv.extract()[0].encode('utf-8')
        clientDescDiv = selector.xpath('//div[@class="news-article-para"]/table/tr[9]/td[4]/div/text()')
        if len(clientDescDiv):
            item["clientDesc"] = clientDescDiv.extract()[0].encode('utf-8')
        else:
            item["clientDesc"] = ""
        yield item
