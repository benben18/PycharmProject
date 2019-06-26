# -*- coding: utf-8 -*-
import scrapy
from stock.items import StockItem

class StocknewsSpider(scrapy.Spider):
    name = 'stocknews'
    allowed_domains = ['stock.10jqka.com.cn']
    start_urls = ['http://stock.10jqka.com.cn/']

    def parse(self, response):
        for i in range(0,1000):
            url = 'http://stock.10jqka.com.cn/companynews_list/index_'+str(i + 1)+'.shtml'

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
        allPageUrl = response.xpath('//div[@class="list-con"]/ul/li/a/@href').extract()
        # print()
        # print(allPageUrl)
        for i in range(0, len(allPageUrl)):  # len(allPageUrl)
            # print(len(allPageUrl))
            # 同样地 将这个页面的url一个一个遍历处理
            yield scrapy.Request(url=allPageUrl[i], callback=self.aNewPage)
            pass
        pass
    # 上一个Request传入的每个新闻的url的响应response即新闻详情页面传入
    #
    def aNewPage(self, response):
        print('正在爬取' + response.url + '信息')
        # 此时要将爬取到的数据存入item中了
        # 引入from news.items import NewsItem 新建item对象
        item = StockItem()
        # 观察页面中所需信息的xpath信息再利用xpath存入对应的item字段
        item['url'] = [response.url]
        a=item['url']
        # print(item['url'][:1])
        # b='stock.10'
        # c='yicai'
        # d='21jingji'
        e='weixin'
        # f='jiemian'
        # g='wabei'
        # h='sohu'
        # if b in a[0]:
        #     print(a[0])
        #     print('nih')
        #     item['title'] = response.xpath('//h2[@class="main-title"]/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//div[@class="main-text atc-content"]/p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )

        # elif c in a[0]:
        #     print(c)
        #     item['title'] = response.xpath('//div[@class="m-list7 f-white"]/h1/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//div[@class="txt"]//p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )
        #
        # elif d in a[0]:
        #     print(d)
        #     item['title'] = response.xpath('//div[@class="titlehead"]/h1/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//div[@class="txtContent"]//p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )

        if e in a[0]:
            print(e)
            item['title'] = response.xpath('//h2[@class="rich_media_title"]/text()').extract()
            print(item['title'])
            content = response.xpath('//div[@class="rich_media_content"]/span/text()').extract()
            # 注意爬取到的content为多段<p>标签组成 需要合并处理
            item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
            print(item['content'] )
        #
        # elif f in a[0]:
        #     print(f)
        #     item['title'] = response.xpath('//div[@class="article-header"]/h1/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//div[@class="article-content"]/p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )
        #
        # elif g in a[0]:
        #     print(g)
        #     item['title'] = response.xpath('//div[@class="subject"]/h1/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//div[@class="subject-content"]/p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )
        #
        # elif h in a[0]:
        #     print(h)
        #     item['title'] = response.xpath('//div[@class="text-title"]/h1/text()').extract()
        #     print(item['title'])
        #     content = response.xpath('//article[@class="article"]/p/text()').extract()
        #     # 注意爬取到的content为多段<p>标签组成 需要合并处理
        #     item['content'] = ["\n".join(content)][0].replace(u'\u3000', u' ')
        #     print(item['content'] )


        # item['time'] = response.xpath('//div[@class="artical-info"]/span/a/span/text()').extract()
        # item['source'] = response.xpath('//div[@class="artical-info"]/span/span/a/text()').extract()
        # item['img'] = response.xpath('//div[@class="artical-importantPic"]/img/@src').extract()
        # content = response.xpath('//div[@class="main-text atc-content"]/p/text()').extract()
        # 注意爬取到的content为多段<p>标签组成 需要合并处理
        # item['content'] = ["\n".join(content)][0].replace(u'\u3000',u' ')
        # 爬取到的数据交给pipelines处理
        yield item


