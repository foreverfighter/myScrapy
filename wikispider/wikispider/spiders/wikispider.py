import scrapy
# scrapy crawl wikipedia -o wikispider.csv
# http://zvon.org/comp/r/tut-XPath_1.html#Pages~List_of_XPaths
# see below for a good example of scraping text with descendants using the descendant-or-self xpath


class WikiSpider(scrapy.Spider):
    name = 'wikipedia'

    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

    def parse(self, response):
        # follow links to author pages
        for href in response.xpath('//b/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_article)

        # # follow pagination links
        # next_page = response.xpath('//div[@id="mw-content-text"]/p/a/@href').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_all_with_xpath(delimiter, query):
            my_list = []
            if response.xpath(query).extract() != None:
                for item in response.xpath(query).extract():
                    if (item != None):
                        my_list.append(item)
                return delimiter.join(my_list)

        yield {
            'topic': extract_with_xpath('//h1[@id="firstHeading"]/text()'),
            'intro': extract_all_with_xpath('', '//div[@id="mw-content-text"]/p[1]/descendant-or-self::*/text()')
        }
