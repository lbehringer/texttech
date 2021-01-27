# --- For reasoning behind the methods below, please see wiki_numbeo_differences.txt. ---


def wiki2numbeo(wiki_subdirectory):
    """returns 2 or 4 values:
    1. the first part of the city name + '-Germany' (only if not identical with 3.)
    2. the first part of the city name (only if not identical with 4.)
    3. the complete city name + '-Germany'
    4. the complete city name"""
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
    """ example input: '/wiki/Berlin'
    this removes '/wiki/' from beginning of string"""
    return wiki_subdirectory[6:]


def remove_segment_after_comma(city):
    """example input: '/wiki/Herne,_North_Rhine-Westphalia'
    returns only the part before the comma"""
    if "," in city:
        parts = city.split(",")
        return parts[0]
    else:
        return city


def replace_umlaut(city):
    """replaces umlauts.
    URL representation of umlauts taken from de.wikipedia.org/wiki/Hilfe:Sonderzeichenreferenz"""
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
    """replaces underscores with hyphens"""
    city_hyphen = city.replace("_", "-")
    return city_hyphen


def capitalize_all(city_hyphen):
    """gets (hyphenated) city name as input
    capitalizes all words and returns 2 values:
    1. complete city name 'city_cap'
    2. first word of city name 'city_cap_first'"""
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
    """adds '-Germany' to numbeo_url"""
    return numbeo_url + "-Germany"


cities = {
    "/wiki/Berlin": 0, "/wiki/Hamburg": 0, "/wiki/Munich": 0, "/wiki/Cologne": 0, "/wiki/Frankfurt": 0, "/wiki/Stuttgart": 0, "/wiki/D%C3%BCsseldorf": 0, "/wiki/Dortmund": 0, "/wiki/Essen": 0, "/wiki/Leipzig": 0, "/wiki/Bremen_(state)": 0, "/wiki/Dresden": 0, "/wiki/Hanover": 0, "/wiki/Nuremberg": 0, "/wiki/Duisburg": 0, "/wiki/Bochum": 0, "/wiki/Wuppertal": 0, "/wiki/Bielefeld": 0, "/wiki/Bonn": 0, "/wiki/M%C3%BCnster": 0, "/wiki/Karlsruhe": 0, "/wiki/Mannheim": 0, "/wiki/Augsburg": 0, "/wiki/Wiesbaden": 0, "/wiki/Gelsenkirchen": 0, "/wiki/M%C3%B6nchengladbach": 0, "/wiki/Braunschweig": 0, "/wiki/Chemnitz": 0, "/wiki/Kiel": 0, "/wiki/Aachen": 0, "/wiki/Halle_(Saale)": 0, "/wiki/Magdeburg": 0, "/wiki/Freiburg_im_Breisgau": 0, "/wiki/Krefeld": 0, "/wiki/L%C3%BCbeck": 0, "/wiki/Oberhausen": 0, "/wiki/Erfurt": 0, "/wiki/Mainz": 0, "/wiki/Rostock": 0, "/wiki/Kassel": 0, "/wiki/Hagen": 0, "/wiki/Hamm": 0, "/wiki/Saarbr%C3%BCcken": 0, "/wiki/M%C3%BClheim_an_der_Ruhr": 0, "/wiki/Potsdam": 0, "/wiki/Ludwigshafen_am_Rhein": 0, "/wiki/Oldenburg_(city)": 0, "/wiki/Leverkusen": 0, "/wiki/Osnabr%C3%BCck": 0, "/wiki/Solingen": 0, "/wiki/Heidelberg": 0, "/wiki/Herne,_North_Rhine-Westphalia": 0, "/wiki/Neuss": 0, "/wiki/Darmstadt": 0, "/wiki/Paderborn": 0, "/wiki/Regensburg": 0, "/wiki/Ingolstadt": 0, "/wiki/W%C3%BCrzburg": 0, "/wiki/F%C3%BCrth": 0, "/wiki/Wolfsburg": 0, "/wiki/Offenbach_am_Main": 0, "/wiki/Ulm": 0, "/wiki/Heilbronn": 0, "/wiki/Pforzheim": 0, "/wiki/G%C3%B6ttingen": 0, "/wiki/Bottrop": 0, "/wiki/Trier": 0, "/wiki/Recklinghausen": 0, "/wiki/Reutlingen": 0, "/wiki/Bremerhaven": 0, "/wiki/Koblenz": 0, "/wiki/Bergisch_Gladbach": 0, "/wiki/Jena": 0, "/wiki/Remscheid": 0, "/wiki/Erlangen": 0, "/wiki/Moers": 0, "/wiki/Siegen": 0, "/wiki/Hildesheim": 0, "/wiki/Salzgitter": 0
    }

numbeo_cities = []
for key in cities.keys():
    numbeo_cities.extend(wiki2numbeo(key))

print(numbeo_cities)
