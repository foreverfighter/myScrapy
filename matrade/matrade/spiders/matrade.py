# scrapy crawl matrade -o matrade.csv
import scrapy
import datetime
# http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=AT&sid=88918A4E72770D712E158F06C4CAF28A
# http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=BM&sid=0C8BA90B85D2543E5E83DE82E26489F0
# http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=BV&sid=1E024743296FFA4AE145776AA0B55522
# http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=EE&sid=430C999DE2A47AA033882351AE83CB15
# http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=MC&sid=5E2D223E54D718054C3F2BA72170F10C
# med 19 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=MD&sid=21226ADD9A6A00C9329164CAAE63271E
# oil 6 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=OS&sid=BE3A5E5C610DA64D157CC4B6F355A67F
# pack 26 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=PK&sid=0EE9FDDC3F7D45C468D41C5A158B90BD
# palm 27 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=PM&sid=D2792FF5DF147539E691E2AFFA091BAA
# plastic 22 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=PS&sid=38E9268629FADD2D697748DF3B6EE637
# food 144 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=FD&sid=606C7A024A159541E2E7D2E89F6A92B9
# rubber 13 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=RB&sid=E8D4005883D5C6511136C07603E9C3E5
# trans 10 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=TP&sid=5C07B458429318449D420E269B2182DC
# wood 26 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=WD&sid=ACBCCB58A9A7F5C89EA4626032418534
# agri 52 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=AG&sid=8575CA08EE7A9E5AA2F75BEB5001B471
# pharma 92 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=PT&sid=BED1E22D5BE3F9B5394D6AF0E742828F
# gloves 10 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=GL&sid=45D7B9E02ADA76B5AC3714C1BB0AD68B
# cons 55 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=EC&sid=44AB6C2B08C720E4889898A15811CB00
# chems 48 http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=CM&sid=BB4ABD2B80A132AFEDCF14A67D95344C


class MatradeSpider(scrapy.Spider):
    name = 'matrade'

    base_url = 'http://edirectory.matrade.gov.my/application/edirectory.nsf/category?OpenForm&query=product&code=CM&sid=BB4ABD2B80A132AFEDCF14A67D95344C&page='
    no_of_catpages = 48
    url_list = []
    for i in range(no_of_catpages):
        url_list.append(base_url + str(i + 1))
    start_urls = url_list

    def parse(self, response):
        # for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div/a[1]/@href').re(r'(.*)(?=&zenid)'):
        # for href in response.xpath('//table[@border="0"]/tbody/tr/td/a/@href').extract():
        # for href in response.xpath('/html/body/form/table[2]/tbody/tr/td[2]/table[2]/tbody/tr/td/a/@href').extract():
        for href in response.xpath('//a/@href').extract():
            if 'profile' in href:
                yield scrapy.Request(response.urljoin(href),
                                     callback=self.parse_copage,
                                     errback=self.errback)

    def errback(self, failure):
        yield {
            'HREF': failure.request.url,
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': repr(failure),
        }

    def parse_copage(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        for i in range(len(response.xpath('//tr/td/b/text()').extract())):
            if 'Business Address' in response.xpath('//tr/td/b/text()').extract()[i]:
                bizadd = response.xpath('//table[@class="company_profile"]//tr[' + str(i + 3) + ']/td[3]/descendant-or-self::*/text()').extract_first()
            if 'Telephone' in response.xpath('//tr/td/b/text()').extract()[i]:
                tel = response.xpath('//table[@class="company_profile"]//tr[' + str(i + 3) + ']/td[3]/descendant-or-self::*/text()').extract_first()
            if 'Email' in response.xpath('//tr/td/b/text()').extract()[i]:
                email = response.xpath('//table[@class="company_profile"]//tr[' + str(i + 3) + ']/td[3]/descendant-or-self::*/text()').extract_first()

        if response.xpath('//font[@size="4"]/text()').extract_first() == None:
            coname = ''
        else:
            coname = response.xpath('//font[@size="4"]/text()').extract_first().strip()

        yield {
            'HREF': response.url,
            'CONAME': coname,
            'BIZADD': bizadd,
            'TEL': tel,
            'EMAIL': email,
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': '',
        }
