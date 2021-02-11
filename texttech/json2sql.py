"""Functions to take the data from json_formatting and turn it into a combined
SQL table"""
import sqlite3
from json_formatting import FORMATTED_NUMBEO, FORMATTED_WIKI


def create_connection(db_name):
    """create a connection to a SQLite database"""
    return sqlite3.connect(db_name)


def create_numbeo_table(c):
    """Creates SQL table for numbeo data with three columns:
    City, Family_of_four, and Single_person"""
    with c:
        c.execute('CREATE TABLE numbeo (City PRIMARY_KEY, Family_of_four INT NOT NULL, Single_person INT NOT NULL);')


def create_wiki_table(c):
    """Creates SQL table for wiki data with five columns:
    City, State, Area, Population, and Density"""
    with c:
        c.execute('CREATE TABLE wiki (City PRIMARY_KEY, State TEXT NOT NULL, Area_km2 INT NOT NULL, Density_km2 INT NOT NULL, Population INT NOT NULL);')


def insert_numbeo_city(c, city_data, show=False):
    """Inserts data from numbeo JSON into numbeo SQL, if show=True, prints the
    table data to the console"""
    with c:
        sql = 'INSERT INTO numbeo VALUES (?, ?, ?)'
        c.execute(sql, city_data)
        if show:
            c.execute('SELECT * FROM numbeo')
            #print(c.fetchall())


def insert_wiki_city(c, city_data, show=False):
    """Inserts data from wiki JSON to wiki SQL, if show=True", prints the table
    data to the console"""
    with c:
        sql = 'INSERT INTO wiki VALUES (?, ?, ?, ?, ?)'
        c.execute(sql, city_data)
        if show:
            c.execute('SELECT * FROM wiki')
            #print(c.fetchall())


def split_numbeo_col(c, show=False):
    """In the numbeo table, creates a new column 'Country' and splits the data
    in the City column appropriately."""
    with c:
        # create new column for the split data to go into
        c.execute('ALTER TABLE numbeo ADD Country')

        # update the table by splitting data in City by the comma
        c.execute('UPDATE numbeo SET Country = SUBSTR(City, INSTR(City, ",")+2)')
        c.execute('UPDATE numbeo SET City = SUBSTR(City, 1, INSTR(City, ",")-1)')

        if show:
            c.execute('SELECT * FROM numbeo')
            #print(c.fetchall())


def join_tables(c, show=False):
    """Joins the numbeo table to the wiki table, where the cities match"""
    with c:
        joint = c.execute('CREATE TABLE joined_table AS SELECT * FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City')
        print(joint.fetchall())
        if show:
            pass
           # print(c.fetchall())


def build_sql_tables(wiki_data, numbeo_data):
    """Function which puts all the other functions together to create the
    tables, insert the data, and join the tables"""
    # create the connection
    conn = create_connection("tables")

    # create the numbeo table and insert data
    create_numbeo_table(conn)
    for each in numbeo_data:
        insert_numbeo_city(conn, list(each.values()), show=False)

    # create the wiki table and insert data
    create_wiki_table(conn)
    for each in wiki_data:
        insert_wiki_city(conn, list(each.values()), show=False)

    # split the numbeo city column > city, country columns
    split_numbeo_col(conn, show=False)

    # join the two tables on the city column
    join_tables(conn, show=True)


if __name__ == '__main__':
    build_sql_tables(FORMATTED_WIKI, FORMATTED_NUMBEO)