from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser


class GitSpider(Spider):
    name = "github"
    allowed_domains = ["github.com"]
    start_urls = ["https://www.github.com/login"]

    def parse(self, response):
        formdata = {'login': 'siowy',
                    'password': 's3cur3PW'}
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        formnumber=1,
                                        clickdata={'name': 'commit'},
                                        callback=self.parse1)

    def parse1(self, response):
        open_in_browser(response)
