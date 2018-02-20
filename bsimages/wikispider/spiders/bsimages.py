import scrapy
import requests

# url = 'https://blacksurvival.gamepedia.com/Items'
# html = urllib.request.urlopen(url).read()

# for src in html.xpath('//td/p/a/img/@src').extract():
#     # img_url = response.urljoin(response.xpath('//img[@id="main-img"]/@src').extract_first())
#     img_url = src.re_first(r'(.*)(?=[?])').strip()  # use this if you need to remove ?foo at the end of the img url
#     item_name = html.xpath('//td/p/a/img/@alt')
#     urllib.request.urlretrieve(img_url, "images/" + item_name)


class BSimagesSpider(scrapy.Spider):
    name = 'bsimages'

    start_urls = ['http://blacksurvival.gamepedia.com/Items']

    def parse(self, response):
        # for href in response.xpath('//div[@class="col-xs-6 col-sm-3"]/div/div/a[1]/@href').re(r'(.*)(?=&zenid)'):
        for src in response.xpath('//td/p/a/img'):
            # img_url = response.urljoin(response.xpath('//img[@id="main-img"]/@src').extract_first())
            img_url = src.xpath('@src').re_first(r'(.*)(?=[?])').strip()  # use this if you need to remove ?foo at the end of the img url
            item_name = src.xpath('@alt').extract_first()
            img_data = requests.get(img_url).content
            saveloc = "images/" + item_name
            with open(saveloc, 'wb') as handler:
                handler.write(img_data)
            # urllib.request.urlretrieve(img_url, "images/" + item_name)
            # img_url = response.xpath('//td/p/a/img/@src').re_first(r'(.*)(?=[?])').strip()  # use this if you need to remove ?foo at the end of the img url
            # item_name = response.xpath('//td/p/a/img/@alt')
            # urllib.request.urlretrieve(img_url, "images/" + item_name)
