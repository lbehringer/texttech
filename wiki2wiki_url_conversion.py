""" returns the complete wikipedia url as opposed to just "/wiki/<cityname>" """


def wiki2wiki(wiki_subdirectory):
    domain = "https://en.wikipedia.org/"
    remove_state(wiki_subdirectory)
    return domain + wiki_subdirectory


def remove_state(wiki_subdirectory):
    if wiki_subdirectory.endswith("_(state)"):
        print(wiki_subdirectory[:-8])
        return wiki_subdirectory[:-8]
    else:
        return wiki_subdirectory
