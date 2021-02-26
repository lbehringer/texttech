# returns the complete wikipedia url as opposed to just "/wiki/<cityname>"


def wiki2wiki(wiki_subdirectory):
    """Since the 'List of cities' in Wikipedia incorrectly contains the link to the state of Bremen
    rather than the city, this corrects the URL so we access the correct data"""
    domain = "https://en.wikipedia.org"
    if wiki_subdirectory.endswith("_(state)"):
        print(wiki_subdirectory[:-8])
        return domain+wiki_subdirectory[:-8]
    else:
        return domain+wiki_subdirectory
