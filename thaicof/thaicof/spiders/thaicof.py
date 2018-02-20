# scrapy crawl thaicof -s LOG_FILE=scrapy.log -o spidergod.csv
import scrapy
import datetime


class ThaicofSpider(scrapy.Spider):
    name = 'thaicof'

    start_urls = ['http://www.thailandcoffee.net/2017/exhibit/exhibiting2017']

    def parse(self, response):
        # for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div/a[1]/@href').re(r'(.*)(?=&zenid)'):
        for href in response.xpath('//td/a/@href').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_product,
                                 errback=self.errback)

    def errback(self, failure):
        yield {
            'HREF': failure.request.url,
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': repr(failure),
        }

    def parse_product(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'HREF': response.url,
            'NAME': response.xpath('//strong[@class="info"]/text()').extract_first().strip(),
            'EMAIL': response.xpath('//span[@class="red"]/text()').extract_first().strip(),
            'DESC': ''.join(response.xpath('//tr[2]/td[1]/div[1]/descendant-or-self::*/text()').extract()).strip(),
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': '',
        }
