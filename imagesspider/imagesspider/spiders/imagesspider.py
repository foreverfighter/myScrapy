import scrapy
import datetime
import urllib


class ImagesSpider(scrapy.Spider):
    name = 'images'

    start_urls = ['https://twilightstrategy.com/card-list/']

    def parse(self, response):
        for href in response.xpath('//table//a/@href').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_card,
                                 errback=self.errback)

    def parse_card(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        img_url = response.xpath('//img[@data-attachment-id]/@src').re_first(r'(.*)(?=[?])').strip()
        if response.xpath('(//strong)[1]/text()').extract_first() == None:
            card_name = response.xpath('(//strong)[2]/text()').extract_first().strip().replace('/', '-')
        else:
            card_name = response.xpath('(//strong)[1]/text()').extract_first().strip().replace('/', '-')
        urllib.request.urlretrieve(img_url, "images/" + card_name + ".jpg")

        yield {
            'HREF': response.url,
            'TIMESTAMP': "'" + str(datetime.date.today()),
            'FAILMSG': '',
        }

    def errback(self, failure):
        yield {
            'HREF': '',
            'TIMESTAMP': '',
            'FAILMSG': repr(failure),
        }
