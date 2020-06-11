from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_footywire_spider(player_list):
    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.


# 'followall' is the name of one of the spiders of the project.
    process.crawl('fw', domain='scrapinghub.com',player_list=player_list)
    process.start() # the script will block here until the crawling is finished