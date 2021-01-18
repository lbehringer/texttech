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
        city_data = {"City": city}

        # keep track of the last row entry, so we know when to nest dictionaries
        last_bullet = ""

        # iterate over the rows in the table
        for row in rows:
            # some of the data we want is in the table heading (th) section
            bullet = row.xpath('th/text()').get()
            if bullet:
                print("b:", bullet)

                # put an entry in the city_data dictionary for the th
                city_data[bullet] = None

                # then get the numberic data from the td field
                number = row.xpath('td/text()').get()

                # often it's None, in which case just keep going
                if number is None:
                    last_bullet = bullet
                    continue

                # some start with a bullet-point, which is this in unicode
                if bullet.startswith('\u00a0\u2022\u00a0'):
                    new = bullet.replace('\u00a0\u2022\u00a0', '')
                    print('new', new)
                    print('last', last_bullet)
                    # that means we need to add it to the previous entry
                    city_data[last_bullet] = {new: number}

                # otherwise, we do a new entry
                else:
                    city_data[bullet] = number
                last_bullet = bullet
                print('#', number)

            else:
                # if it's a heading, also print it
                heading = row.xpath('th/a/text()').get()
                if heading is None:
                    continue
                text = row.xpath('td/a/text()').get()
                print("h:", heading)
                if text is None:
                    continue
                print("txt:", text)
                city_data[heading] = text
        yield city_data


class NumbeoSpider(scrapy.Spider):
    name = 'numbeo'
    start_urls = ['https://www.numbeo.com/cost-of-living/in/Stuttgart']

    def parser(self, response):
        path = response.xpath('/html/body/div[2]/div[2]')


if __name__ == '__main__':
    pass