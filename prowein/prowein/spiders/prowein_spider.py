import scrapy
# scrapy crawl prowein -o prowein.csv
# scrapy crawl prowein -s JOBDIR=crawls/prowein-1 -o prowein.csv


class ProweinSpider(scrapy.Spider):
    name = "prowein"
    start_urls = ['http://www.prowein.com/vis/v1/en/directory/a?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/b?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/c?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/d?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/e?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/f?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/g?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/h?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/i?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/j?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/k?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/l?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/m?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/n?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/o?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/p?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/q?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/r?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/s?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/t?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/u?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/v?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/w?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/x?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/y?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/z?oid=29558&lang=2',
                  'http://www.prowein.com/vis/v1/en/directory/other?oid=29558&lang=2']

    def parse(self, response):
        # follow links to entry pages
        for href in response.xpath('//div[@class="exh-table-col exh-table-col--name"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_exhibitor_entry)  # this is used if the href is a partial href
            # yield scrapy.Request(href,
            #                      callback=self.parse_exhibitor_entry)

        # # follow pagination links
        # next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        # if next_page is not None:
        #     # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_exhibitor_entry(self, response):
        def extract_with_xpath(query):
            if (response.xpath(query).extract_first() != None):
                return response.xpath(query).extract_first().strip()
            else:
                return None

        # def extract_all_with_xpath(delimiter, query):
        #     my_list = []
        #     for item in response.xpath(query).extract():
        #         if (item != None):
        #             my_list.append(item.strip())
        #     return delimiter.join(my_list)

        yield {
            'exhibitor_name': extract_with_xpath('//h1[@itemprop="name"]/text()'),
            'email': extract_with_xpath('//a[@itemprop="email"]/@href')
        }
