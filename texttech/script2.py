import json
import os
from scrapy.crawler import CrawlerProcess
from texttech.spiders.first_spider import WikiSpider, NumbeoSpider
from wiki2wiki_url_conversion import wiki2wiki
from wiki2numbeo_url_conversion import wiki2numbeo
from json_formatting import format_wiki_data, format_numbeo_data, load_json
from json2sql import build_sql_tables


def clear_json(file_name):
    """
    Removes json file if it already exists
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


def numbeo_tuples_to_list(incomplete_urls):
    """
    Converts the tuples of numbeo-url variants to a list
    """
    numbeo_urls = []
    for city in incomplete_urls:
        try:
            url1, url2, url3, url4 = wiki2numbeo(city)
            numbeo_urls.append(url1)
            numbeo_urls.append(url2)
            numbeo_urls.append(url3)
            numbeo_urls.append(url4)
        except:
            url1, url2 = wiki2numbeo(city)
            numbeo_urls.append(url1)
            numbeo_urls.append(url2)
    return numbeo_urls


def convert_urls():
    """
    Converts entries in "urls.json" to functional URLs for WikiSpider and NumbeoSpider
    """
    incomplete_urls = read_json("urls.json")
    wiki_urls = [wiki2wiki(city) for city in incomplete_urls]
    numbeo_urls = numbeo_tuples_to_list(incomplete_urls)
    return wiki_urls, numbeo_urls


def run_wiki_numbeo_spiders():
    """
    Assigns functional URLs as start_urls for the respective spiders,
    clears existing json files and runs WikiSpider and NumbeoSpider
    """
    wiki_urls, numbeo_urls = convert_urls()
    clear_json("wiki.json")
    clear_json("numbeo.json")
    process = CrawlerProcess()
    process.crawl(WikiSpider, start_urls=wiki_urls)
    process.crawl(NumbeoSpider, start_urls=numbeo_urls)
    process.start()
    return None


run_wiki_numbeo_spiders()
# read data from files "numbeo.json" and "wiki.json" and format it for entry into SQL tables
NUMBEO_DATA = load_json('numbeo.json')
FORMATTED_NUMBEO = format_numbeo_data(NUMBEO_DATA)
WIKI_DATA = load_json('wiki.json')
FORMATTED_WIKI = format_wiki_data(WIKI_DATA)
#create sql tables from formatted data
build_sql_tables(FORMATTED_WIKI, FORMATTED_NUMBEO)
