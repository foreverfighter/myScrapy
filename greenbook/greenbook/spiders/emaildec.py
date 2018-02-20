# scrapy crawl greenbook -s LOG_FILE=scrapy.log -o spidergod.csv
import scrapy


class DecSpider(scrapy.Spider):
    name = 'dec'
    # start_urls = ['http://www.thegreenbook.com/']
    # for testing
    start_urls = ['http://www.thegreenbook.com/companies/disco-hi-tec-s-pte-ltd/']

    # def parse(self, response):
    #     for href in response.xpath('//div[@id="classificationIndex"]/div[@class="content"]/div/div[@class="ID-list"]/ul/li/a/@href').extract():
    #         yield scrapy.Request(href,
    #                              callback=self.parse_subcatpage,
    #                              errback=self.errback)

    def parse(self, response):
        # self.logger.info('Ran parse_subcatpage')
        # for href in response.xpath('//div[@id="div_Search_Results_Found"]/div/h2/p/a/@href').extract():
        hidcompemail = response.xpath('//input[@id="hidCompEmail"]/@value').extract_first()
        yield scrapy.Request('http://www.thegreenbook.com/companyprofile.aspx/DecryptEmail',
                             body="{sEmail: '" + hidcompemail + "'}",
                             method='POST',
                             headers={
                                 # 'Accept': 'application/json, text/javascript, */*; q=0.01',
                                 # 'Accept-Encoding': 'gzip, deflate',
                                 # 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                                 # 'Content-Length': 56,
                                 'Content-Type': 'application/json',
                                 # 'Cookie': 'ASP.NET_SessionId=2buet2j2bxdi0t45kbcvueiw; __utmt=1; __utma=165539962.21733179.1496728954.1496728954.1496728954.1; __utmb=165539962.1.10.1496728954; __utmc=165539962; __utmz=165539962.1496728954.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __atuvc=1%7C23; __atuvs=593645795694a223000',
                                 # 'Host': 'www.thegreenbook.com',
                                 # 'Origin': 'http://www.thegreenbook.com',
                                 # 'Referer': 'http://www.thegreenbook.com/companies/disco-hi-tec-s-pte-ltd/',
                             },
                             callback=self.parse_email)

    def parse_email(self, response):
        yield {
            'email': response.body
        }

    # def parse_listing(self, response):
    #     for href in response.xpath('//a[@itemprop="CompanyName"]/@href').extract():
    #         yield scrapy.Request(href,
    #                              callback=self.parse_company,
    #                              errback=self.errback,
    #                              meta={'bigcat': response.meta['bigcat'],
    #                                    'smallcat': response.url
    #                                    })

        # if response.xpath('//div[@class="numberNagivation"]/a[@class="active"]/text()').extract_first() is not None:
        #     current_page = int(response.xpath('//div[@class="numberNagivation"]/a[@class="active"]/text()').extract_first())
        #     next_page = current_page + 1
        #     next_page_url = response.meta['url'] + 'page/{}/'.format(str(next_page))
        #     if response.xpath('//a[@id="pagernext"]/@class') is not "disabled":
        #         yield scrapy.Request(next_page_url,
        #                              callback=self.parse_listing,
        #                              errback=self.errback,
        #                              meta={'url': response.meta['url'],
        #                                    'bigcat': href})
    #     if response.meta['page'] == 1:
    #         category_url = response.url
    #     else:
    #         category_url = response.meta['category url']

    #     if response.xpath('//div[@id="error404"]').extract_first() is None:
    #         next_page = str(1 + int(response.meta['page']))
    #         next_page_url = category_url + 'page/' + next_page + '/'
    #         yield scrapy.Request(next_page_url,
    #                              callback=self.parse_listing,
    #                              errback=self.errback,
    #                              meta={'bigcat': response.meta['bigcat'],
    #                                    'page': next_page,
    #                                    'category url': category_url})

    # def parse_company(self, response):
    #     def extract_with_xpath(query):
    #         return response.xpath(query).extract_first().strip()

    #     if response.xpath('//div[@class="breadcrumb"]/h1/text()').extract_first() is not None:
    #         coname = response.xpath('//div[@class="breadcrumb"]/h1/text()').extract_first().strip()
    #     else:
    #         coname = ""

    #     if response.xpath('//a[@class="viewEmailBtn"]/span[@class="viewEmail"]/text()').extract_first() is not None:
    #         email = response.xpath('//a[@class="viewEmailBtn"]/span[@class="viewEmail"]/text()').extract_first().strip()
    #     else:
    #         email = ""

    #     if response.xpath('//span[@class="phoneNum"]/text()').extract_first() is not None:
    #         phone = response.xpath('//span[@class="phoneNum"]/text()').extract_first().strip()
    #     else:
    #         phone = ""

    #     if response.xpath('//span[@class="faxNum"]/text()').extract_first() is not None:
    #         fax = response.xpath('//span[@class="faxNum"]/text()').extract_first().strip()
    #     else:
    #         fax = ""

    #     if response.xpath('//span[@itemprop="CompanyAddress"]/text()').extract_first() is not None:
    #         coaddress = response.xpath('//span[@itemprop="CompanyAddress"]/text()').extract_first().strip()
    #     else:
    #         coaddress = ""

    #     # if response.xpath('//div[@class="profile"]/descendant-or-self::*/text()').extract() is not None:
    #     #     profile = '\n\n'.join(response.xpath('//div[@class="profile"]/descendant-or-self::*/text()').extract())
    #     # else:
    #     #     profile = ""

    #     yield {
    #         'HREF': response.url,
    #         'CONAME': coname,
    #         'EMAIL': email,
    #         'PHONE': phone,
    #         'FAX': fax,
    #         'ADDRESS': coaddress,
    #         # 'PROFILE': profile,
    #         'FAILMSG': '',
    #         'BIGCAT': response.meta['bigcat'],
    #         'SMALLCAT': response.meta['smallcat']
    #     }

    # def errback(self, failure):
    #     yield {
    #         'HREF': failure.request.url,
    #         'FAILMSG': repr(failure),
    #     }
