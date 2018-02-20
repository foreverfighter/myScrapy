import scrapy
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, MapCompose
from twilightstrategy.items import TwilightstrategyItem

# scrapy crawl somespider -s JOBDIR=crawls/somespider-1

# to run, type "scrapy crawl ieat -o ieat.csv"
# self.logger.info("Visited %s", response.url)
# def parse_page1(self, response):
#     item = MyItem()
#     item['main_url'] = response.url
#     request = scrapy.Request("http://www.example.com/some_page.html",
#                              callback=self.parse_page2)
#     request.meta['item'] = item
#     yield request

# def parse_page2(self, response):
#     item = response.meta['item']
#     item['other_url'] = response.url
#     yield item


# see below for errback logging/yielding
# yield scrapy.Request(u, callback=self.parse_httpbin,
#                         errback=self.errback_httpbin,
#                         dont_filter=True)
# def errback_httpbin(self, failure):
#     # log all failures
#     self.logger.error(repr(failure))

# try items!!!!
# try link extractor!
# try media pipeline!
#    from scrapy.linkextractors import LinkExtractor
# and passing items between pages using the meta tag!

# class LoginSpider(scrapy.Spider):
#     name = 'example.com'
#     start_urls = ['http://www.example.com/users/login.php']

#     def parse(self, response):
#         return scrapy.FormRequest.from_response(
#             response,
#             formdata={'username': 'john', 'password': 'secret'},
#             callback=self.after_login
#         )

#     def after_login(self, response):
#         # check login succeed before going on
#         if "authentication failed" in response.body:
#             self.logger.error("Login failed")
#             return

# custom_settings = {
#     'SOME_SETTING': 'some value',
# }

# DEPTH_PRIORITY
# Default: 0

# Scope: scrapy.spidermiddlewares.depth.DepthMiddleware

# An integer that is used to adjust the request priority based on its depth:

# if zero (default), no priority adjustment is made from depth
# a positive value will decrease the priority, i.e. higher depth requests will be processed later ; this is commonly used when doing breadth-first crawls (BFO)
# a negative value will increase priority, i.e., higher depth requests will be processed sooner (DFO)

# from myproject.items import MyItem

class TwilightLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # name_in = MapCompose(strip)
    # time_in = MapCompose(strip)
    # side_in = MapCompose(strip)
    # ops_in = MapCompose(strip)
    # removed_in = MapCompose(strip)


class TwilightSpider(scrapy.Spider):
    name = 'twilight3'

    start_urls = ['https://twilightstrategy.com/card-list/']
    # AUTOTHROTTLE_ENABLED = True
    ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
    IMAGES_STORE = '/images'

    def parse(self, response):
        # follow links to card pages
        for href in response.xpath('//table//a/@href').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_card,
                                 errback=self.errback)

    def errback(self, failure):
        self.logger.error(repr(failure))
        l = TwilightLoader(item=TwilightstrategyItem(), response=response)
        l.add_value('href', failure.request.url)
        l.add_value('failmsg', repr(failure))
        return l.load_item()
        # yield {
        #     #            'FAILURL': failure.request.url,
        #     'FAILMSG': repr(failure)
        # }
        # # follow pagination links
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_card(self, response):
        # self.logger.info('Visited {}'.format(response.url))
        l = TwilightLoader(item=TwilightstrategyItem(), response=response)
        l.add_value('href', response.url)
        l.add_xpath('name', '//h2[@class="entry-title"]/a/text()')
        l.add_xpath('time', '//div[@class="entry-content"]/p[3]/text()[1]')
        l.add_xpath('side', '//div[@class="entry-content"]/p[3]/text()[3]')
        l.add_xpath('ops', '//div[@class="entry-content"]/p[3]/text()[5]')
        l.add_xpath('removed', '//div[@class="entry-content"]/p[3]/text()[7]')
        l.add_xpath('image_urls', '//img[@data-attachment-id]/@src')
        l.add_value('timestamp', str(datetime.datetime.now()))
        return l.load_item()

        # def extract_with_xpath(query):
        #     return response.xpath(query).extract_first().strip()

        # yield {
        #     'HREF': response.url,
        #     'NAME': extract_with_xpath('//h2[@class="entry-title"]/a/text()'),
        #     'TIME': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[1]'),
        #     'SIDE': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[3]'),
        #     'OPS': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[5]'),
        #     'REMOVED': extract_with_xpath('//div[@class="entry-content"]/p[3]/text()[7]'),
        #     # 'FAILURL': '',
        #     'FAILMSG': '',
        # }
