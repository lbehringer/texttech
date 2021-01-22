# returns the complete wikipedia url as opposed to just "/wiki/<cityname>"


def wiki2wiki(wiki_subdiretory):
    domain = "https://en.wikipedia.org/"
    return domain+wiki_subdiretory