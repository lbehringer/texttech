# --- For reasoning behind the methods below, please see wiki_numbeo_differences.txt. ---


def wiki2numbeo(wiki_subdirectory):
    """
    Returns 2 or 4 values:
    1. the first part of the city name + '-Germany' (only if not identical with 3.)
    2. the first part of the city name (only if not identical with 4.)
    3. the complete city name + '-Germany'
    4. the complete city name
    """
    numbeo_domain = "https://www.numbeo.com/cost-of-living/in/"
    wiki_city = get_wiki_city(wiki_subdirectory)
    wiki_city = remove_segment_after_comma(wiki_city)
    wiki_city = replace_umlaut(wiki_city)
    wiki_city = replace_underscore(wiki_city)
    numbeo_city_first, numbeo_city = capitalize_all(wiki_city)

    # 4 variants to try (in the order they are returned).
    numbeo_url_first = numbeo_domain + numbeo_city_first
    numbeo_first_country = specify_country(numbeo_url_first)
    numbeo_url = numbeo_domain + numbeo_city
    numbeo_url_country = specify_country(numbeo_url)

    # Only return all 4 variants if numbeo_url_first and numbeo_first_country
    # are different from numbeo_city and numbeo_country.
    if numbeo_city_first != numbeo_city:
        return numbeo_first_country, numbeo_url_first, numbeo_url_country, numbeo_url
    else:
        return numbeo_url_country, numbeo_url


def get_wiki_city(wiki_subdirectory):
    """
    Example input: '/wiki/Berlin'
    This removes '/wiki/' from beginning of string
    """
    return wiki_subdirectory[6:]


def remove_segment_after_comma(city):
    """
    Example input: '/wiki/Herne,_North_Rhine-Westphalia'
    Returns only the part before the comma
    """
    if "," in city:
        parts = city.split(",")
        return parts[0]
    else:
        return city


def replace_umlaut(city):
    """
    Replaces umlauts.
    URL representation of umlauts taken from de.wikipedia.org/wiki/Hilfe:Sonderzeichenreferenz
    """
    city = city.replace("Ä", "A")
    city = city.replace("%C3%84", "A")
    city = city.replace("Ö", "O")
    city = city.replace("%C3%96", "O")
    city = city.replace("Ü", "U")
    city = city.replace("%C3%9C", "U")
    city = city.replace("ß", "ss")
    city = city.replace("%C3%9F", "ss")
    city = city.replace("ä", "a")
    city = city.replace("%C3%A4", "a")
    city = city.replace("ö", "o")
    city = city.replace("%C3%B6", "o")
    city = city.replace("ü", "u")
    city = city.replace("%C3%BC", "u")
    return city


def replace_underscore(city):
    """
    Replaces underscores with hyphens
    """
    city_hyphen = city.replace("_", "-")
    return city_hyphen


def capitalize_all(city_hyphen):
    """
    gets (hyphenated) city name as input
    capitalizes all words and returns 2 values:
    1. complete city name 'city_cap'
    2. first word of city name 'city_cap_first'
    """
    parts = city_hyphen.split("-")
    city_cap = ''
    city_cap_first = ''
    for i in range(len(parts)):
        parts[i] = parts[i].capitalize()
    for part in parts:
        if part == parts[0]:
            city_cap_first = part
        city_cap += part
        if part != parts[-1]:
            city_cap += "-"
 
    return city_cap_first, city_cap


def specify_country(numbeo_url):
    """
    adds '-Germany' to numbeo_url
    """
    return numbeo_url + "-Germany"
