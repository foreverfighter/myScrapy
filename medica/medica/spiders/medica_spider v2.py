import scrapy
# scrapy crawl medica -o medica.csv
# scrapy crawl medica -s JOBDIR=crawls/medica-1 -o medica.csv


class MedicaSpider2(scrapy.Spider):
    name = "medica2"
    start = 0
    results_base_url = 'http://www.medica-tradefair.com/vis-api/vis/v1/de/search/slice?oid=80396&lang=2&_query=&f_type=profile&f_prod=medcom2016.MEDICA.01*&_start={}&_rows=20'
    start_urls = [results_base_url.format('0')]
    download_delay = 1.5
    # start_urls = ['http://www.medica-tradefair.com/vis-api/vis/v1/de/search/slice?oid=80396&lang=2&_query=&f_type=profile&f_prod=medcom2016.MEDICA.01*&_start=0&_rows=3000']

    def parse(self, response):
        yield {
            'response': response.body
            # 'exhibitor_name': extract_with_xpath('//h1[@itemprop="name"]/text()'),
            # 'email': extract_with_xpath('//a[@itemprop="email"]/text()')
        }
        # follow links to entry pages
        # this is used if the href is a partial href
        # for href in response.xpath('//div[@class="searchresult-item  searchresult-item--tol "]/a/@href').extract():
        #     yield scrapy.Request(response.urljoin(href),
        #                          callback=self.parse_exhibitor_entry)  # this is used if the href is a partial href
        # yield scrapy.Request(href,
        #                      callback=self.parse_exhibitor_entry)

        # # follow pagination links
        # next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        # if next_page is not None:
        #     # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_results(self, response):
        for href in response.xpath('//div[@class="searchresult-item  searchresult-item--tol "]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_exhibitor_entry)  # this is used if the href is a partial href

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
            'email': extract_with_xpath('//a[@itemprop="email"]/text()')
        }
