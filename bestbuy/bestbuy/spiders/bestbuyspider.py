import scrapy
import datetime
import urllib


class BestBuySpider(scrapy.Spider):
    name = 'bestbuy'

    start_urls = ['http://sg.bestbuy-world.com/index.php?main_page=products_brand&brand=&cPath=0&manufacturers_id=0&sort=4d&min_price=5&max_price=500']

    def parse(self, response):
        # for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div/a[1]/@href').re(r'(.*)(?=&zenid)'):
        for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div[@class="product-thumb-wrapper"]/a[1]/@href').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_product,
                                 errback=self.errback)

        next_page = response.xpath('//a[@title=" Next Page "]/@href').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
            yield scrapy.Request(next_page, callback=self.parse, errback=self.errback)

    def errback(self, failure):
        yield {
            'HREF': failure.request.url,
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': repr(failure),
        }

    def parse_product(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        img_url = response.urljoin(response.xpath('//img[@id="main-img"]/@src').extract_first())
        # img_url = response.xpath('//img[@id="main-img"]/@src').re_first(r'(.*)(?=[?])').strip()  # use this if you need to remove ?foo at the end of the img url
        product_name = ' '.join(response.xpath('//p[@class="product-name"]/text()').extract()).strip().replace('/', '-').replace('?', '')
        urllib.request.urlretrieve(img_url, "images/" + product_name + ".jpg")

        if response.xpath('//span[@class=" old-price"]/text()').extract_first() == None:
            old_price = ''
        else:
            old_price = response.xpath('//span[@class=" old-price"]/text()').extract_first().strip()

        yield {
            'HREF': response.url,
            'ID': response.xpath('//p[@class="new-price"]/text()').re_first(r'Product ID: (\d+)'),
            'BRAND': response.xpath('//p[@class="product-name"]/a/text()').extract_first().strip(),
            'NAME': product_name,
            'OLD_PRICE': old_price,
            'NEW_PRICE': response.xpath('//span[@class="price"]/text()').extract_first().strip(),
            'DESC': '\n\n'.join(response.xpath('//div[@class="para"]/descendant-or-self::*/text()').extract()),
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': '',
        }
