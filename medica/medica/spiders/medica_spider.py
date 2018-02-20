import scrapy
# i stopped at 1500
# 6086 total hits to scrape based on http://www.medica-tradefair.com/vis/v1/en/search?oid=80396&lang=2&f_type=profile&_query=&lang=2&ticket=g_u_e_s_t&oid=80794

# scrapy crawl medica -o medica2.csv
# scrapy crawl medica -s JOBDIR=crawls/medica-1 -o medica.csv
# import os
# os.environ["http_proxy"] = "http://localhost:8118"


class MedicaSpider(scrapy.Spider):
    name = "medica"
    urls = []
    for i in range(9999):
        urls.append('http://www.medica-tradefair.com/vis/v1/de/exhibitors/medcom2016.246{:04.0f}?oid=80396&lang=2&_query=&f_type=profile&f_prod=medcom2016.MEDICA.01*'.format(i))
        # urls.append('http://www.medica-tradefair.com/vis/v1/de/exhibitors/medcom2016.250{:04.0f}?oid=80396&lang=2&_query=&f_type=profile&f_prod=medcom2016.MEDICA.01*'.format(i))

    start_urls = urls

    def parse(self, response):
        def extract_with_xpath(query):
            if (response.xpath(query).extract_first() != None):
                return response.xpath(query).extract_first().strip()
            else:
                return None

        yield {
            'exhibitor_name': extract_with_xpath('//h1[@itemprop="name"]/text()'),
            'email': extract_with_xpath('//a[@itemprop="email"]/text()')
        }
