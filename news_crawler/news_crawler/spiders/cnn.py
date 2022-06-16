from dataclasses import replace
from tracemalloc import start
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import NewsArticle

class cnn_spider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['cnn.com']

    start_urls = ['https://edition.cnn.com/india']

    rules= [Rule(LinkExtractor(allow=r'\/2022\/[0-9][0-9]\/[0-9][0-9]\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'),
    callback='parse_item', follow=True)]

    def parse_item(self, response):
        article = NewsArticle()
        article['url'] = response.url
        article['source'] = 'CNN'
        article['title'] = response.xpath('//h1/text()').get()
        article['description'] = response.xpath('//meta[@name="description"]/@content').get()
        article['date'] = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        article['author'] = response.xpath('//meta[@itemprop="author"]/@content').get().replace(', CNN', '')
        article['text'] = response.xpath('//section[@data-zone-label="bodyText"]/div[@class="l-container"]//*/text()').getall()
        return article