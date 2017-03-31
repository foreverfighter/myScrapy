import scrapy


class IEatSpider(scrapy.Spider):
    name = "ieat"
    start_urls = ['http://ieatishootipost.sg/category/eat/']

    def parse(self, response):
        # follow links to entry pages
        for href in response.xpath('//h3[@class="entry-title"]/a/@href').extract():
            # yield scrapy.Request(response.urljoin(href),
            #                      callback=self.parse_rname)  #this is used if the href is a partial href
            yield scrapy.Request(href,
                                 callback=self.parse_rname)

        # follow pagination links
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_rname(self, response):
        def extract_with_xpath(query):
            if (response.xpath(query).extract_first() != None):
                return response.xpath(query).extract_first().strip()
            else:
                return None

        def extract_all_with_xpath(delimiter, query):
            my_list = []
            for item in response.xpath(query).extract():
                if (item != None):
                    my_list.append(item.strip())
            return delimiter.join(my_list)

        yield {
            'restname': extract_with_xpath('//p[@class="restaurant-name"]/text()'),
            'address': extract_with_xpath('//div[@class="cc-column address"]/div[@class="info"]/text()[2]'),
            'opening hours': extract_all_with_xpath('\n', '//div[@class="cc-column opening-hours"]/descendant::*/text()'),
            'contact': extract_with_xpath('//div[@class="cc-column phone-contact last"]/div[@class="info"]/text()[2]'),
            'rating': extract_all_with_xpath(', ', '//span[@style="color: #ff0000;"]/text()'),
            'conclusion': extract_all_with_xpath('\n', '//div[@class="article-content"]/p[last()]/text()') + ', ' + extract_all_with_xpath(', ', '//span[@style="color: #ff0000;"]/descendant::*/text()'),
            # conclusion extraction is imperfect, next attempt, to get the index of the p element of 'conclusion', and then extract text of p+1
            'tags': extract_all_with_xpath(', ', '//div[@class="categories text-color-dark text-small"]/descendant::*/text()')
        }
