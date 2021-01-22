import re

# returns 4 values: 
# the first part of the city name + "-Germany"
# the first part of the city name
# the complete city name + "-Germany"
# the complete city name
def wiki2numbeo(wiki_subdirectory):
    numbeo_domain = "numbeo.com/cost-of-living/in/"
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

# example wiki subdirectory: /wiki/Regensburg
# example numbeo URL: numbeo.com/cost-of-living/in/Regensburg
# just start the URL string with numbeo domain 
# remove "/wiki/" from start
def get_wiki_city(wiki_subdirectory):
    return wiki_subdirectory[6:]


# Wiki sometimes links cities with e.g. Bundesland information after a comma
# whereas numbeo doesn't.
# /wiki/Herne,_North_Rhine-Westphalia
def remove_segment_after_comma(city):
    if "," in city:
        parts = city.split(",")
        return parts[0]
    else:
        return city

# Wiki has Umlaute, numbeo doesn't: 
# "/wiki/Saarbrücken", "numbeo.../Saarbrucken"
# de.wikipedia.org/wiki/Hilfe:Sonderzeichenreferenz
# could perhaps formulate this more efficiently
def replace_umlaut(city):
    city_no_umlaut = city
    city_no_umlaut = city_no_umlaut.replace("Ä", "A")
    city_no_umlaut = city_no_umlaut.replace("%C3%84", "A")
    city_no_umlaut = city_no_umlaut.replace("Ö", "O")
    city_no_umlaut = city_no_umlaut.replace("%C3%96", "O")
    city_no_umlaut = city_no_umlaut.replace("Ü", "U")
    city_no_umlaut = city_no_umlaut.replace("%C3%9C", "U")
    city_no_umlaut = city_no_umlaut.replace("ß", "ss")
    city_no_umlaut = city_no_umlaut.replace("%C3%9F", "ss")
    city_no_umlaut = city_no_umlaut.replace("ä", "a")
    city_no_umlaut = city_no_umlaut.replace("%C3%A4", "a")
    city_no_umlaut = city_no_umlaut.replace("ö", "o")
    city_no_umlaut = city_no_umlaut.replace("%C3%B6", "o")
    city_no_umlaut = city_no_umlaut.replace("ü", "u")
    city_no_umlaut = city_no_umlaut.replace("%C3%BC", "u")
    return city_no_umlaut


# 
# Wiki splits words with underscore, numbeo with hyphen:
# "/wiki/Freiburg_im_Breisgau", "numbeo.../Freiburg-Im-Breisgau"
def replace_underscore(city):
    city_hyphen = city.replace("_", "-")
    return city_hyphen

# numbeo capitalizes all words in city names that consist of more than 1 word:
# "wiki/Offenbach_am_Main", "numbeo.../Offenbach-Am-Main-Germany"
# --> capitalize all words after getting wiki URL as input
# --> input already has hyphens instead of underscores
# returns two values: complete city name "city_cap"
# and first word of city name "city_cap_first"
def capitalize_all(city_hyphen):
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


# on numbeo, some cities have a "-Germany" after the city name
# --> create if loop: if "Kassel" doesn't exist, try appending "-Germany"
# if this also doesn't exist, skip this city
def specify_country(numbeo_url):
    return numbeo_url + "-Germany"


cities = {
    "/wiki/Berlin": 0, "/wiki/Hamburg": 0, "/wiki/Munich": 0, "/wiki/Cologne": 0, "/wiki/Frankfurt": 0, "/wiki/Stuttgart": 0, "/wiki/D%C3%BCsseldorf": 0, "/wiki/Dortmund": 0, "/wiki/Essen": 0, "/wiki/Leipzig": 0, "/wiki/Bremen_(state)": 0, "/wiki/Dresden": 0, "/wiki/Hanover": 0, "/wiki/Nuremberg": 0, "/wiki/Duisburg": 0, "/wiki/Bochum": 0, "/wiki/Wuppertal": 0, "/wiki/Bielefeld": 0, "/wiki/Bonn": 0, "/wiki/M%C3%BCnster": 0, "/wiki/Karlsruhe": 0, "/wiki/Mannheim": 0, "/wiki/Augsburg": 0, "/wiki/Wiesbaden": 0, "/wiki/Gelsenkirchen": 0, "/wiki/M%C3%B6nchengladbach": 0, "/wiki/Braunschweig": 0, "/wiki/Chemnitz": 0, "/wiki/Kiel": 0, "/wiki/Aachen": 0, "/wiki/Halle_(Saale)": 0, "/wiki/Magdeburg": 0, "/wiki/Freiburg_im_Breisgau": 0, "/wiki/Krefeld": 0, "/wiki/L%C3%BCbeck": 0, "/wiki/Oberhausen": 0, "/wiki/Erfurt": 0, "/wiki/Mainz": 0, "/wiki/Rostock": 0, "/wiki/Kassel": 0, "/wiki/Hagen": 0, "/wiki/Hamm": 0, "/wiki/Saarbr%C3%BCcken": 0, "/wiki/M%C3%BClheim_an_der_Ruhr": 0, "/wiki/Potsdam": 0, "/wiki/Ludwigshafen_am_Rhein": 0, "/wiki/Oldenburg_(city)": 0, "/wiki/Leverkusen": 0, "/wiki/Osnabr%C3%BCck": 0, "/wiki/Solingen": 0, "/wiki/Heidelberg": 0, "/wiki/Herne,_North_Rhine-Westphalia": 0, "/wiki/Neuss": 0, "/wiki/Darmstadt": 0, "/wiki/Paderborn": 0, "/wiki/Regensburg": 0, "/wiki/Ingolstadt": 0, "/wiki/W%C3%BCrzburg": 0, "/wiki/F%C3%BCrth": 0, "/wiki/Wolfsburg": 0, "/wiki/Offenbach_am_Main": 0, "/wiki/Ulm": 0, "/wiki/Heilbronn": 0, "/wiki/Pforzheim": 0, "/wiki/G%C3%B6ttingen": 0, "/wiki/Bottrop": 0, "/wiki/Trier": 0, "/wiki/Recklinghausen": 0, "/wiki/Reutlingen": 0, "/wiki/Bremerhaven": 0, "/wiki/Koblenz": 0, "/wiki/Bergisch_Gladbach": 0, "/wiki/Jena": 0, "/wiki/Remscheid": 0, "/wiki/Erlangen": 0, "/wiki/Moers": 0, "/wiki/Siegen": 0, "/wiki/Hildesheim": 0, "/wiki/Salzgitter": 0
    }

numbeo_cities = []
for key in cities.keys():
    numbeo_cities.extend(wiki2numbeo(key))

print(numbeo_cities)