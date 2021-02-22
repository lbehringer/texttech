"""Functions to transform data from scraper output to SQL input"""
import json
import re

digit_pattern = re.compile(r'[\d.,]+')
alpha_pattern = re.compile(r'[\S]+')


def load_json(file_name):
    """
    Takes the name of a file in string format and returns the data in the file
    as a list (currently only works if the file is in the same location as this
    python file)
    """
    with open(file_name) as f:
        file = json.load(f)
    return file


def get_digit(string):
    """
    function which uses regex to find digits in a string, also removes
    commas so that they can be cast to float type
    """
    digit = re.findall(digit_pattern, string)[0]
    digit = digit.replace(',', '')
    return digit


def get_alpha(string):
    """
    function which uses regex to find digits in a string, also removes
    commas so that they can be cast to float type
    """
    alpha = re.findall(alpha_pattern, string)[0]
    return alpha


def remove_umlaut(string):
    """
    Takes a string and replaces vowels-with-umlauts with vowels-without-umlauts
    """
    string = string.replace('ü', 'u')
    string = string.replace('ö', 'o')
    string = string.replace('ä', 'a')
    string = string.replace('ï', 'i')
    string = string.replace('ë', 'e')
    string = string.replace('Ä', 'A')
    string = string.replace('Ë', 'E')
    string = string.replace('Ï', 'I')
    string = string.replace('Ö', 'O')
    string = string.replace('Ü', 'U')
    return string


def format_numbeo_data(numbeo_data):
    """
    Takes the list of JSON formatted numbeo data (i.e. dictionaries of strings),
    removes blank entries, removes euro symbols, and casts numbers as floats.
    """
    formatted = []

    # iterate over each entry in the data
    for entry in numbeo_data:
        # if it's blank, just skip it
        if not entry["City"]:
            continue

        # otherwise get the numeric data and cast it as float
        else:
            family_cost = float(get_digit(entry["Family_of_four"]))
            single_cost = float(get_digit(entry["Single_person"]))
            # then put it back together and add to list of formatted data
            formatted_entry = [entry["City"], family_cost, single_cost]
            if formatted_entry not in formatted:
                formatted.append(formatted_entry)
    return formatted


def format_wiki_data(wiki_data):
    """
    Takes the list of JSON formatted wiki data and removes units of measure,
    also extracts data from the nested population dictionary to make it easier
    to access.
    """
    # ISSUE: there are three weird entries that don't have proper city names

    formatted = []

    for entry in wiki_data:
        # get the city name
        city = get_wiki_city(entry)

        # get the state name
        state = get_wiki_state(entry, city)

        # get just area in km2, not unit or miles
        area = get_wiki_area(entry)

        # population and density are a nested dictionary, extract these
        density, population = get_wiki_popdensity(entry, area)
        formatted_entry = [city, state, area, density, population]
        formatted.append(formatted_entry)
    return formatted


def get_wiki_city(entry):
    """
    Takes a single wikipedia data entry and returns the city name without any
    extra white spaces
    """
    city = get_alpha(entry["City_name"])
    return city


def get_wiki_state(entry, city):
    """
    Takes a single wikipedia data entry and returns the state name
    """
    if city in ["Berlin", "Hamburg"]:
        state = city
    else:
        try:
            state = entry["State"]
        except KeyError:
            print(entry)
    return state


def get_wiki_area(entry):
    """
    Takes a single wikipedia data entry and returns the area field as a float
    """
    if type(entry["Area"]) == str:
        area = get_digit(entry["Area"])
    elif "Total" in entry["Area"]:
        area = get_digit(entry["Area"]["Total"])
    elif "City" in entry["Area"]:
        area = get_digit(entry["Area"]["City"])
    else:
        area = get_digit(entry["Area"]["City/State"])
    return float(area)


def get_wiki_popdensity(entry, area):
    """
    Takes a single wikipedia data entry and returns the population and density
    fields as integers
    """
    # Density and Population are nested inside a dictionary called Population
    pop_dict = entry["Population"]
    for k, v in pop_dict.items():
        if k == "Density":
            density = get_digit(pop_dict[k])

        # the population value isn't always called the same thing, but it's
        # always the other dictionary entry
        else:
            population = get_digit(pop_dict[k])
    # Berlin doesn't have density info; calculate it from area and population
    if len(pop_dict) == 1:
        density = int(population)/area
    return int(density), int(population)


# read data from file and format it for entry into SQL tables
NUMBEO_DATA = load_json('numbeo.json')
FORMATTED_NUMBEO = format_numbeo_data(NUMBEO_DATA)
WIKI_DATA = load_json('wiki.json')
FORMATTED_WIKI = format_wiki_data(WIKI_DATA)
