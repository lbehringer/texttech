# returns the complete wikipedia url as opposed to just "/wiki/<cityname>"

CITIES = {
    "/wiki/Berlin": 0, "/wiki/Hamburg": 0, "/wiki/Munich": 0, "/wiki/Cologne": 0, "/wiki/Frankfurt": 0, "/wiki/Stuttgart": 0, "/wiki/D%C3%BCsseldorf": 0, "/wiki/Dortmund": 0, "/wiki/Essen": 0, "/wiki/Leipzig": 0, "/wiki/Bremen": 0, "/wiki/Dresden": 0, "/wiki/Hanover": 0, "/wiki/Nuremberg": 0, "/wiki/Duisburg": 0, "/wiki/Bochum": 0, "/wiki/Wuppertal": 0, "/wiki/Bielefeld": 0, "/wiki/Bonn": 0, "/wiki/M%C3%BCnster": 0, "/wiki/Karlsruhe": 0, "/wiki/Mannheim": 0, "/wiki/Augsburg": 0, "/wiki/Wiesbaden": 0, "/wiki/Gelsenkirchen": 0, "/wiki/M%C3%B6nchengladbach": 0, "/wiki/Braunschweig": 0, "/wiki/Chemnitz": 0, "/wiki/Kiel": 0, "/wiki/Aachen": 0, "/wiki/Halle_(Saale)": 0, "/wiki/Magdeburg": 0, "/wiki/Freiburg_im_Breisgau": 0, "/wiki/Krefeld": 0, "/wiki/L%C3%BCbeck": 0, "/wiki/Oberhausen": 0, "/wiki/Erfurt": 0, "/wiki/Mainz": 0, "/wiki/Rostock": 0, "/wiki/Kassel": 0, "/wiki/Hagen": 0, "/wiki/Hamm": 0, "/wiki/Saarbr%C3%BCcken": 0, "/wiki/M%C3%BClheim_an_der_Ruhr": 0, "/wiki/Potsdam": 0, "/wiki/Ludwigshafen_am_Rhein": 0, "/wiki/Oldenburg_(city)": 0, "/wiki/Leverkusen": 0, "/wiki/Osnabr%C3%BCck": 0, "/wiki/Solingen": 0, "/wiki/Heidelberg": 0, "/wiki/Herne,_North_Rhine-Westphalia": 0, "/wiki/Neuss": 0, "/wiki/Darmstadt": 0, "/wiki/Paderborn": 0, "/wiki/Regensburg": 0, "/wiki/Ingolstadt": 0, "/wiki/W%C3%BCrzburg": 0, "/wiki/F%C3%BCrth": 0, "/wiki/Wolfsburg": 0, "/wiki/Offenbach_am_Main": 0, "/wiki/Ulm": 0, "/wiki/Heilbronn": 0, "/wiki/Pforzheim": 0, "/wiki/G%C3%B6ttingen": 0, "/wiki/Bottrop": 0, "/wiki/Trier": 0, "/wiki/Recklinghausen": 0, "/wiki/Reutlingen": 0, "/wiki/Bremerhaven": 0, "/wiki/Koblenz": 0, "/wiki/Bergisch_Gladbach": 0, "/wiki/Jena": 0, "/wiki/Remscheid": 0, "/wiki/Erlangen": 0, "/wiki/Moers": 0, "/wiki/Siegen": 0, "/wiki/Hildesheim": 0, "/wiki/Salzgitter": 0
    }


def wiki2wiki(wiki_subdiretory):
    domain = "https://en.wikipedia.org"
    return domain+wiki_subdiretory


wiki_cities = [wiki2wiki(city) for city in CITIES.keys()]
