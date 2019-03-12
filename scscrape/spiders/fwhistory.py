# -*- coding: utf-8 -*-
import scrapy
import re
from scscrape.items import PlayerItem
from scscrape.items import YearItem
MAX = 1000

class FwhistorySpider(scrapy.Spider):
    name = 'fwhistory'
    allowed_domains = ['footywire.com']
    start_urls = ['https://www.footywire.com/afl/footy/ft_players']
    DOWNLOAD_DELAY = 0.75

    # must return an iterable of Requests (you can return a list of requests or write a generator function)
    # which the Spider will begin to crawl from.
    # Subsequent requests will be generated successively from these initial requests.


    def parse(self, response):
        i = 0

        #self.log(response.css('td.lnormtop a::attr(href)').getall())

        for player in response.css('td.lnormtop a::attr(href)').getall():
            next_page = player
            if next_page is not None:
                next_page = response.urljoin(next_page)
                i += 1
                if i > MAX:
                    break
                #yield one then other
                yield scrapy.Request(next_page, callback=self.parse_player_info)
                #yield scrapy.Request(next_page, callback=self.parse_player)


    def parse_player_info(self, response5):
        #self.log('I just visited' + response2.url)

        item = PlayerItem()
        item['name'] = response5.xpath('//h3[@id = "playerProfileName"]/text()').get()
        # item['info_team'] = response2.xpath('//div[@id = "playerProfileTeamDiv"]/text()').get()
        item['info1'] = response5.xpath('//div[@id = "playerProfileData1"]/text()').get()
        item['info2'] = response5.xpath('//div[@id = "playerProfileData2"]/text()').get()
        item['info_draft'] = response5.xpath('//div[@id = "playerProfileDraftInfo"]/text()').get()
        item['sc_price'] = response5.xpath('//div[@id = "playerProfileSupercoach"]/text()').get()
        yield item # Yeild one set of items at a time


    def parse_player(self, response2):
        self.log('I just visited' + response2.url)

        """item = PlayerItem()
        item['name'] = response2.xpath('//h3[@id = "playerProfileName"]/text()').get()
        #item['info_team'] = response2.xpath('//div[@id = "playerProfileTeamDiv"]/text()').get()
        item['info1'] = response2.xpath('//div[@id = "playerProfileData1"]/text()').get()
        item['info2'] = response2.xpath('//div[@id = "playerProfileData2"]/text()').get()
        item['info_draft'] =response2.xpath('//div[@id = "playerProfileDraftInfo"]/text()').get()
        item['sc_price'] = response2.xpath('//div[@id = "playerProfileSupercoach"]/text()').get()
        yield item # Yeild one set of items at a time"""

        # Determine number of Games
        string = response2.css('#playerProfileData1').get()

        index = string.index("Games")
        #print(index)
        numbergames = re.findall('\d+', string[index:index + 12])
        #print(numbergames)

        if numbergames[0] != 0:
            next_page_2 = response2.css('#playerProfileSupercoach a::attr(href)').get()
            if next_page_2 is not None:
                #print("NEXT PAGE " + next_page_2)
                next_page_2 = response2.urljoin(next_page_2)
                yield scrapy.Request(next_page_2, callback=self.parse_supercoach)

    def parse_supercoach(self, response3):
        #print('SUPERCOACH DATA\n')
        self.log('I just visited' + response3.url)



        for link in response3.xpath('//table[@width=298]//@href').extract():

            if "pg" in link and link is not None:
                print("NEXT PAGE " + link)
                link = response3.urljoin(link)
                yield scrapy.Request(link, callback=self.parse_supercoachyear)

    def parse_supercoachyear(self, response4):

        i = 1;
        round = None
        date = None
        opponent = None
        result = None
        AF = None
        SC = None


        heading = response4.xpath('//table[@width=998]/tr[1]/td/text()|//table[@width=998]/tr[1]/th/text()').getall()
        length = len(heading)

        for i in range(length):
            #print(i)
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


        item = YearItem()
        item['info'] = response4.xpath('//table/tr/td[@class ="tbtitle"]/text()').getall()
        item['round_array'] = response4.xpath('//table[@width=998]/tr/td[' + round + ']/text()').getall()
        item['date_array'] = response4.xpath('//table[@width=998]/tr/td[' + date + ']/text()').getall()
        item['opponent_array'] = response4.xpath('//table[@width=998]/tr/td[' + opponent + ']/a/text()').getall()
        item['result_array'] = response4.xpath('//table[@width=998]/tr/td[' + result + ']/a/text()').getall()
        item['AFscore_array'] = response4.xpath('//table[@width=998]/tr/td[' + AF + ']/text()').getall()
        item['SCscore_array'] = response4.xpath('//table[@width=998]/tr/td[' + SC + ']/text()').getall()

        yield item
