"""SQL queries that answer the story questions about cities and cost of living
in Germany. Note: the tables.db file needs to be in the same location as this
python file in order for it to run correctly."""
import sqlite3


def get_top_density_low_cost(c):
    """select the five cities with the highest density, that have a single
     person cost of living under 750 euro a month. Return fields: cities,
     density, and single person cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT city, density_km2, single_person '
            'FROM joined_table '
            'WHERE single_person < 750 '
            'ORDER BY density_km2 DESC '
            'LIMIT 5')
        return cursor.fetchall()


def get_highest_family_cost(c):
    """select the city with the highest monthly living cost for a family of
    four. Return fields: city, area, population, density, and cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT city, area_km2, population, density_km2, MAX(family_of_four) '
            'FROM joined_table ')
        return cursor.fetchall()


def get_lowest_single_cost(c):
    """select the city with the highest monthly living cost for a family of
        four. Return fields: city, area, population, density, and cost"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT city, area_km2, population, density_km2, MIN(single_person) '
            'FROM joined_table ')
        return cursor.fetchall()


def get_total_area(c):
    """select the total area in km2 of all the cities that we collected."""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT SUM(area_km2) '
            'FROM joined_table ')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


def get_average_cost(c):
    """select the average monthly living cost for a family of four"""
    with c:
        cursor = c.cursor()
        cursor.execute(
            'SELECT AVG(family_of_four) '
            'FROM joined_table ')
        # this returns a tuple in a list, so let's index in to get the number
        return cursor.fetchall()[0][0]


if __name__ == '__main__':
    c = sqlite3.connect('tables')
    top_5 = get_top_density_low_cost(c)
    max_cost = get_highest_family_cost(c)
    min_cost = get_lowest_single_cost(c)
    print(min_cost)
    total_area = get_total_area(c)
    # print to 2 decimal points
    print("Total area: %.2f" % total_area)
    avg_cost = get_average_cost(c)
    print("Average family cost (Euro): %.2f" % avg_cost)