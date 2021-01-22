import sqlite3
import json
import re

digit_pattern = re.compile(r'[\d.,]+')


def create_connection(db_name):
    return sqlite3.connect(db_name)


def create_numbeo_table(c):
    with c:
        c.execute('CREATE TABLE numbeo (City TEXT PRIMARY_KEY, Family_of_four '
                  'INT NOT NULL, Single_person INT NOT NULL);')


def create_wiki_table(c):
    with c:
        c.execute('CREATE TABLE wiki (City TEXT PRIMARY_KEY, State TEXT NOT NULL, '
                  'Area_km2 INT NOT NULL, Elevation_metres INT NOT NULL, '
                  'Population INT NOT NULL, Density_km2 INT NOT NULL);')


def load_json(file_name):
    with open(file_name) as f:
        file = json.load(f)
    return file


def get_digit(string):
    digit = re.findall(digit_pattern, string)[0]
    digit = digit.replace(',', '')
    return digit


def remove_umlaut(string):
    string = string.replace('ü', 'u')
    string = string.replace('ö', 'o')
    string = string.replace('ä', 'a')
    string = string.replace('ï', 'i')
    string = string.replace('ë', 'e')
    string = string.replace('Ä', 'A')
    string = string.replace('Ë', 'E')
    string = string.replace('Ï', 'I')
    string = string.replace('Ö', 'O')
    string = string.replace('Ü', 'U')
    return string


def format_numbeo_data(numbeo_data):
    formatted = list(numbeo_data)
    pass


def format_wiki_data(wiki_data):

    formatted = list(wiki_data)

    for idx, entry in enumerate(wiki_data):
        # get just area in km2, not unit or miles
        area = get_digit(entry["Area"]["Total"])
        formatted[idx]["Area"] = float(area)

        # get just elevation in m, not unit or feet
        elevation = get_digit(formatted[idx]["Elevation"])
        formatted[idx]["Elevation"] = int(elevation)

        # possible issue: will Population always be followed by (2019-12-31)?
        pop_dict = formatted[idx]["Population (2019-12-31)"]
        for k, v in pop_dict.items():
            if k == "Density":
                density = get_digit(pop_dict[k])
                formatted[idx][k] = int(density)
            else:
                formatted[idx]["Population"] = get_digit(pop_dict[k])
        del formatted[idx]["Population (2019-12-31)"]

    return formatted


def insert_numbeo_city(c, city_data, show=False):
    with c:
        sql = 'INSERT INTO numbeo VALUES (?, ?, ?)'
        c.execute(sql, city_data)
        if show:
            c.execute('SELECT * FROM numbeo')
            #print(c.fetchall())


def insert_wiki_city(c, city_data, show=False):
    with c:
        sql = 'INSERT INTO wiki VALUES (?, ?, ?, ?, ?, ?)'
        c.execute(sql, city_data)
        if show:
            c.execute('SELECT * FROM wiki')
            #print(c.fetchall())


def split_numbeo_col(c, show=False):
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
    with c:
        joint = c.execute('SELECT * FROM wiki LEFT OUTER JOIN numbeo ON numbeo.City = wiki.City')
        print(joint.fetchall())
        if show:
            pass
           # print(c.fetchall())


if __name__ == '__main__':
    numbeo_data = load_json('mock_numbeo')
    conn = create_connection("numbeo")
    create_numbeo_table(conn)
    for each in numbeo_data:
        insert_numbeo_city(conn, list(each.values()), show=False)
    wiki_data = load_json('mock_wiki')
    formatted = format_wiki_data(wiki_data)
    create_wiki_table(conn)
    for each in wiki_data:
        insert_wiki_city(conn, list(each.values()), show=False)
    split_numbeo_col(conn, show=False)
    join_tables(conn, show=True)