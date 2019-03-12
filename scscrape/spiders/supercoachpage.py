import scrapy
import re
from scscrape.items import PlayerItem
MAX = 4

class SupercoachPage(scrapy.Spider):
    name = 'SuperCoachPage'
    allowed_domains = ['footywire.com']
    start_urls = ['https://www.footywire.com/afl/footy/pg-geelong-cats--gary-jnr-ablett?year=2007&fantasy=y']
    download_delay = 2

    # must return an iterable of Requests (you can return a list of requests or write a generator function)
    # which the Spider will begin to crawl from.
    # Subsequent requests will be generated successively from these initial requests.


    def parse(self, response):


        i = 1;
        round = None
        date = None
        opponent = None
        result = None
        AF = None
        SC = None

        #print(response.xpath('//table[@width=998]/tr[1]/td/text()|//table[@width=998]/tr[1]/th/text()').getall())

        #get header
        heading = response.xpath('//table[@width=998]/tr[1]/td/text()|//table[@width=998]/tr[1]/th/text()').getall()
        length = len(heading)

        for i in range(length):
            print(i)
            if 'Description' in heading[i]:
                round = str(i + 1)

            elif heading[i] == 'Date':
                date = str(i + 1)

            elif heading[i] == 'Opponent':
                opponent = str(i + 1)

            elif heading[i] == 'Result':
                result = str(i + 1)

            elif heading[i] == 'AF':
                AF = str(i + 1)

            elif heading[i] == 'SC':
                SC = str(i + 1)











        #get index for each part
        #return index
        print(response.xpath('//table/tr/td[@class ="tbtitle"]/text()').getall())
        print(response.xpath('//table[@width=998]/tr/td[' + round + ']/text()').getall()) #position() = $round]
        print(response.xpath('//table[@width=998]/tr/td[' + date + ']/text()').getall())
        print(response.xpath('//table[@width=998]/tr/td[' + opponent + ']/a/text()').getall())
        print(response.xpath('//table[@width=998]/tr/td[' + result + ']/a/text()').getall())
        print(response.xpath('//table[@width=998]/tr/td[' + AF + ']/text()').getall())
        print(response.xpath('//table[@width=998]/tr/td[' + SC + ']/text()').getall())
