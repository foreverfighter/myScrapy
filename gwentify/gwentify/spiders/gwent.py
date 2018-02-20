# scrapy crawl myspider -s LOG_FILE=scrapy.log

import scrapy
import datetime


class GwentifySpider(scrapy.Spider):
    name = 'gwentify'

    start_urls = ['http://gwentify.com/card-category/faction/nilfgaard/',
                  'http://gwentify.com/card-category/faction/skellige/',
                  'http://gwentify.com/card-category/faction/scoiatael/',
                  'http://gwentify.com/card-category/faction/northern-realms/']
# http://gwentify.com/card-category/faction/neutral/
# http://gwentify.com/card-category/faction/monster/

    def parse(self, response):
        # for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div/a[1]/@href').re(r'(.*)(?=&zenid)'):
        cards_in_page = len(response.xpath('//div[@class="col-md-24 meta-box halfpad bordered"]').extract())
        for i in range(cards_in_page):
            yield {
                'CARDNAME': ''.join(response.xpath('(//h2[@class="entry-title"])[{}]/a/text()'.format(str(i + 1))).extract()),
                'STRENGTH': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[1]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'GROUP': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[2]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'RARITY': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[3]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'LOYALTY': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[4]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'FACTION': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[5]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'POSITION': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[6]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'TYPE': ''.join(response.xpath('(//ul[@class="card-cats"])[{}]/li[7]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
                'TEXT': ''.join(response.xpath('(//div[@class="card-text"])[{}]/descendant-or-self::*/text()'.format(str(i + 1))).extract()),
            }

        next_page = response.xpath('//a[@class="nextpostslink"]/@href').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
            yield scrapy.Request(next_page, callback=self.parse, errback=self.errback)

    def errback(self, failure):
        yield {
            'HREF': failure.request.url,
            'DATE_SCRAPED': "'" + str(datetime.date.today()),
            'FAILMSG': repr(failure),
        }

    # def parse_product(self, response):
    #     def extract_with_xpath(query):
    #         return response.xpath(query).extract_first().strip()

    #     img_url = response.urljoin(response.xpath('//img[@id="main-img"]/@src').extract_first())
    #     # img_url = response.xpath('//img[@id="main-img"]/@src').re_first(r'(.*)(?=[?])').strip()  # use this if you need to remove ?foo at the end of the img url
    #     product_name = ' '.join(response.xpath('//p[@class="product-name"]/text()').extract()).strip().replace('/', '-').replace('?', '')
    #     urllib.request.urlretrieve(img_url, "images/" + product_name + ".jpg")

    #     if response.xpath('//span[@class=" old-price"]/text()').extract_first() == None:
    #         old_price = ''
    #     else:
    #         old_price = response.xpath('//span[@class=" old-price"]/text()').extract_first().strip()

    #     yield {
    #         'HREF': response.url,
    #         'ID': response.xpath('//p[@class="new-price"]/text()').re_first(r'Product ID: (\d+)'),
    #         'BRAND': response.xpath('//p[@class="product-name"]/a/text()').extract_first().strip(),
    #         'NAME': product_name,
    #         'OLD_PRICE': old_price,
    #         'NEW_PRICE': response.xpath('//span[@class="price"]/text()').extract_first().strip(),
    #         'DESC': '\n\n'.join(response.xpath('//div[@class="para"]/descendant-or-self::*/text()').extract()),
    #         'DATE_SCRAPED': "'" + str(datetime.date.today()),
    #         'FAILMSG': '',
    #     }
