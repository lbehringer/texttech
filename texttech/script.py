import scrapy
import os
import json
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from texttech.spiders.first_spider import urlSpider, WikiSpider, NumbeoSpider
from wiki2wiki_url_conversion import wiki2wiki
from wiki2numbeo_url_conversion import wiki2numbeo



# remove already existing json files to prevent duplicates and format errors
def clear_json(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    return None


def read_json(file_name):
    """
    :param file_name: string that matches the path to the json (probably urls.json)
    :return: list of strings of urls
    """
    # to make this work, the json file must be in the same location as the spider/script

    with open(file_name) as f:
        f = json.load(f)
    url_dict = f[0]
    urls = [key for key, value in url_dict.items()]
    return urls


# outputs the results of urlSpider to a file "urls.json"
url_process = CrawlerProcess()
wiki_numbeo_process = CrawlerProcess()

clear_json("urls.json")
url_process.crawl(urlSpider)
url_process.start()

#run_wiki_numbeo_spiders()


# # use urls.json for WikiSpider and NumbeoSpider
# incomplete_urls = read_json("urls.json")
#
# # convert incomplete_urls to wiki_urls and numbeo_urls
# wiki_urls = [wiki2wiki(city) for city in incomplete_urls]
# numbeo_urls = [wiki2numbeo(city) for city in incomplete_urls]
#
# print(wiki_urls)
# print(numbeo_urls)
#
# wiki_numbeo_process.crawl(WikiSpider, start_urls=wiki_urls)
# wiki_numbeo_process.start(stop_after_crawl=False)
# wiki_numbeo_process.crawl(NumbeoSpider, start_urls=numbeo_urls)
# wiki_numbeo_process.start(stop_after_crawl=True)

#configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#runner = CrawlerRunner()
#wiki_numbeo_process = CrawlerProcess()


"""Failed attempt with CrawlerRunner"""
# clear_json("urls.json")
# d = runner.crawl(urlSpider)
# d.addboth(lambda _: reactor.stop())
# reactor.run()
#
#
# # use urls.json for WikiSpider and NumbeoSpider
# incomplete_urls = read_json("urls.json")
#
# # convert incomplete_urls to wiki_urls and numbeo_urls
# wiki_urls = [wiki2wiki(city) for city in incomplete_urls]
# numbeo_urls = [wiki2numbeo(city) for city in incomplete_urls]
#
# print(wiki_urls)
# print(numbeo_urls)
#
# wiki_numbeo_process.crawl(WikiSpider, start_urls=wiki_urls)
# wiki_numbeo_process.start(stop_after_crawl=False)
# wiki_numbeo_process.crawl(NumbeoSpider, start_urls=numbeo_urls)
# wiki_numbeo_process.start(stop_after_crawl=True)