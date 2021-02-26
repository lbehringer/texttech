import os
import json
from scrapy.crawler import CrawlerProcess
from texttech.spiders.first_spider import urlSpider


def clear_json(file_name):
    """
    Removes already existing json files to prevent duplicates and format errors
    """
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


# crawl urls and output the results of urlSpider to a file "urls.json"
url_process = CrawlerProcess()
clear_json("urls.json")  # clears "urls.json" if it already exists to avoid format errors
url_process.crawl(urlSpider)
url_process.start()
