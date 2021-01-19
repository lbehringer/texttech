import scrapy


class WikiSpider(scrapy.Spider):
    """
    spider to get city data from Wikipedia pages
    """
    name = "wiki"
    start_urls = ['https://en.wikipedia.org/wiki/Stuttgart']
    # custom settings to save results to a json file
    custom_settings = {'FEED_URI': "wiki.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        # set rows to xpath for the table with the city info
        rows = response.xpath('//table[@class="infobox geography vcard"]/tbody/tr')

        # first extract the city name, which has it's own particular xpath
        city = rows.xpath('th/div/span/text()').get()
        city_data = {"City_name": city}

        # keep track of the last row entry, so we know when to nest dictionaries
        last_bullet = ""

        # iterate over the rows in the table
        for row in rows:
            # some of the data we want is in the table heading (th) section
            heading = row.xpath('th/text()').get()
            if heading:
                # then get the numeric data from the td field
                number = row.xpath('td/text()').get()

                # often it's None, in which case just keep going
                if number is None:
                    last_bullet = heading
                    continue

                # some start with a bullet-point, which is this in unicode
                # if it's a bullet, it's a value for the previous heading key
                if heading.startswith('\u00a0\u2022\u00a0'):
                    bullet = heading.replace('\u00a0\u2022\u00a0', '')
                    # if there's nothing left, just skip
                    if not bullet:
                        continue
                    # check if there's a previous entry
                    if last_bullet in city_data:
                        # if there is, add an extra value to the previous entry
                        city_data[last_bullet][bullet] = number
                    # or create the first value for the previous entry
                    else:
                        city_data[last_bullet] = {bullet: number}

                # if it's not , we do a new entry
                else:
                    city_data[heading] = number
                    last_bullet = heading

            else:
                # if it's a heading in /a/ section, also get it
                heading = row.xpath('th/a/text()').get()
                # if it's empty, just skip
                if heading is None:
                    continue

                # get the associated numeric data
                text = row.xpath('td/a/text()').get()
                # if it's empty, just skip
                if text is None:
                    continue

                # add both to the city data dictionary
                city_data[heading] = text

        yield city_data


class NumbeoSpider(scrapy.Spider):
    name = 'numbeo'
    start_urls = ['https://www.numbeo.com/cost-of-living/in/Stuttgart']
    # custom settings to save results to a json file
    custom_settings = {'FEED_URI': "numbeo.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        path = response.xpath('/html/body/div[2]/div[2]')
        city = path.xpath('p/span[@class="purple_light"]/text()').get()
        four = path.xpath('ul/li[1]/span/text()').get()
        single = path.xpath('ul/li[2]/span/text()').get()
        print('done')
        print(city, four, single)
        yield {'City': city, 'Family_of_four': four, "Single_person": single}


if __name__ == '__main__':
    pass