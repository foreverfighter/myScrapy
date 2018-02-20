import scrapy
# to run, type "scrapy crawl ieat -o ieat.csv"


class TwilightSpider(scrapy.Spider):
    name = 'twilight'

    start_urls = ['https://twilightstrategy.com/card-list/']

    def parse(self, response):
        # follow links to card pages
        for href in response.xpath('//table//a/@href').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_card)

        # # follow pagination links
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_card(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'NAME': extract_with_xpath('//h2[@class="entry-title"]/a/text()'),
            'TIME': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[1]'),
            'SIDE': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[3]'),
            'OPS': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[5]'),
            'REMOVED': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[7]'),
        }
