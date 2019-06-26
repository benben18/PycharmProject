# -*- coding: utf-8 -*-
import scrapy
from sinaeconews.items import SinaeconewsItem

class SinaecoSpider(scrapy.Spider):
    name = 'sinaeco'
    allowed_domains = ['finance.sina.com.cn']
    start_urls = ['http://finance.sina.com.cn']
    def parse(self, response):
        for i in range(0,25):
            url = 'http://finance.sina.com.cn/roll/index.d.html?cid=56592&page='+str(i + 1)
            # yield类似于这个数的return后循环在下一个数执行
            # Request(url,callback)用于迭代爬取 可以调用callback进一步爬取传入的url
            # 记得引入from scrapy.http import Request
            # 这个语句的意思是 将每个遍历到的url做进一步处理再执行下一个遍历到的url
            yield scrapy.Request(url=url, callback=self.newsPage)
        pass
    # 上一个Request传入的url响应的response作为参数传入回调函数newsPage

    def newsPage(self, response):
        # 通过观察页面我们知道每个页面中的新闻的连接在
        # 属性为class=list-hd的div标签下的h4标签下的a标签下的href属性中
        # 可用response.xpath().extract()得到这个页面所有新闻的url
        allPageUrl = response.xpath('//ul[@class="list_009"]/li/a/@href').extract()

        print(allPageUrl)
        for i in range(0, len(allPageUrl)):  # len(allPageUrl)

            print(len(allPageUrl))
            # 同样地 将这个页面的url一个一个遍历处理
            yield scrapy.Request(url=allPageUrl[i], callback=self.aNewPage)
            pass
        pass
    # 上一个Request传入的每个新闻的url的响应response即新闻详情页面传入

    def aNewPage(self, response):
        # 此时要将爬取到的数据存入item中了
        # 引入from news.items import NewsItem 新建item对象
        item = SinaeconewsItem()
        # 观察页面中所需信息的xpath信息再利用xpath存入对应的item字段
        item['url'] = [response.url]

        # print(item['url'])

        item['title'] = response.xpath('//h1[@class="main-title"]/text()').extract()
        # print(item['title'])

        # item['time'] = response.xpath('//div[@class="artical-info"]/span/a/span/text()').extract()
        # item['source'] = response.xpath('//div[@class="artical-info"]/span/span/a/text()').extract()
        # item['img'] = response.xpath('//div[@class="artical-importantPic"]/img/@src').extract()
        content = response.xpath('//div[@class="article"]//p/text()').extract()
        # 注意爬取到的content为多段<p>标签组成 需要合并处理
        item['content'] = ["\n".join(content)][0].replace(u'\u3000',u' ')
        # 爬取到的数据交给pipelines处理
        yield item





