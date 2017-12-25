import scrapy
from bs4 import *
from tutorial.items import TutorialItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.txtjia.com/shu/43014/9485346.html",
        # "http://localhost:8080/liao/"
    ]
    # def parse(self, response):
    #     print("123")
    #     for sel in response.xpath("//"):
    #         print(sel.xpath('').extract())
    def parse(self, response):
        for sel in response.xpath("//div[@class='content']"):
            item = TutorialItem()
            item['text'] = sel.extract()
            nei = BeautifulSoup(item['text'], "html.parser")
            text = nei.select('#booktext')[0].get_text()
            Title1 = nei.select('dt h1')[0].get_text()
            item['Title'] = Title1
            item['text'] = text
            # text = nei.select("#booktext").get_text()
            # Title = nei.select("").get_text()
            #item['Title'] = BeautifulSoup(item['text'], "html.parser").select("dt h1").get_text()
            #item['link'] = sel.xpath('@href').extract()
            #print(item['title'])
            yield item
        next_page = response.xpath('//li/a')
        next_page=next_page.xpath('@href')

        # for x in  range(8,len(next_page)):
        #     print("456")
        url = response.urljoin( next_page[len(next_page)-1].extract())
        print(url)
        # 爬每一页
        yield scrapy.Request(url,dont_filter=True, callback=self.parse)