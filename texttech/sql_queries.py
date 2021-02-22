"""SQL queries that answer the story questions about cities and cost of living
in Germany. Note: the tables.db file needs to be in the same location as this
python file in order for it to run correctly."""
import sqlite3
from os import linesep


def get_top_density_low_cost(c):
    """select the five cities with the highest density, that have a single
     person cost of living under 750 euro a month. Return fields: cities,
     density, and single person cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT wiki.city, density_km2, single_person '
            'FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City '
            'WHERE single_person < 750 '
            'ORDER BY density_km2 DESC '
            'LIMIT 5')
        return cursor.fetchall()


def get_highest_family_cost(c):
    """select the city with the highest monthly living cost for a family of
    four where the density is < 1500 people per square km.
    Return fields: city and cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT wiki.city, MAX(family_of_four) '
            'FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City '
            'WHERE density_km2 < 1500')
        return cursor.fetchall()


def get_lowest_single_cost(c):
    """select the city with the lowest monthly living cost for a single person
     and a population over 300,000. Return fields: city, population, and cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT wiki.city, MIN(single_person) '
            'FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City '
            'WHERE population > 300000')
        return cursor.fetchall()


def get_total_area(c):
    """select the total area in km2 of all the cities that we collected."""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT SUM(area_km2) '
            'FROM wiki')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


def get_avg_family_cost(c):
    """select the average monthly living cost for a family of four"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT AVG(family_of_four) '
            'FROM numbeo')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


def get_avg_single_cost(c):
    """select the average monthly living cost for a single person"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT AVG(single_person) '
            'FROM numbeo')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


def get_avg_sg_cost_NRW(c):
    """select the average monthly living cost for a single person in the state
    of North Rhine-Westphalia"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT AVG(single_person) '
            'FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City '
            'WHERE state="North Rhine-Westphalia"')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


def get_avg_fam_cost_NRW(c):
    """select the average monthly living cost for a single person in the state
    of North Rhine-Westphalia"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT AVG(family_of_four) '
            'FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City '
            'WHERE state="North Rhine-Westphalia"')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


if __name__ == '__main__':
    c = sqlite3.connect('tables')
    top_5 = get_top_density_low_cost(c)
    top_5_cities = [data[0] for data in top_5]
    max_cost = get_highest_family_cost(c)
    min_cost = get_lowest_single_cost(c)
    total_area = get_total_area(c)
    avg_fam_cost = get_avg_family_cost(c)
    avg_fam_NRW_cost = get_avg_fam_cost_NRW(c)
    avg_sg_cost = get_avg_single_cost(c)
    avg_sg_NRW_cost = get_avg_sg_cost_NRW(c)
    print("Five highest density cities that have a cost of living below 750"
          "euro per month for a single person:")
    print(", ".join(top_5_cities), linesep)
    print("City with the highest monthly cost of living for a family of four "
          "and density below 1500 people per square km:")
    print("%s. Cost in euro: %s" % max_cost[0], linesep)
    print("City with the lowest monthly cost of living for a single person "
          "and population over 300,000:")
    print("%s. Cost in euro: %s" % min_cost[0], linesep)
    print("Total area of the cities in our database in square kilometres:")
    print("%.2f" % total_area, linesep)
    print("Average monthly family cost in euro: %.2f" % avg_fam_cost)
    print("Average monthly family person cost in euro in NRW: %.2f" %
          avg_fam_NRW_cost)
    print("Average monthly single person cost in euro: %.2f" % avg_sg_cost)
    print("Average monthly single person cost in euro in NRW: %.2f" %
          avg_sg_NRW_cost)
