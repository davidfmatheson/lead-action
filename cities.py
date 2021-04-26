import csv

from mysql.connector import connect, Error
from jproperties import Properties

def find_city_id(city, county, state):
    city_id = -1
    configs = Properties()

    with open("data/db.properties", "rb") as config_file:
        configs.load(config_file)
        db_host = configs["DB_HOST"].data
        db_name = configs["DB_NAME"].data
        db_user = configs["DB_USER"].data
        db_pass = configs["DB_PASS"].data

        try:
            with connect(host = db_host, database = db_name, user = db_user, password = db_pass) as connection:
                query = f"SELECT COUNT(ci.id) as city_id_count FROM state st, county co, city ci WHERE st.id = co.state_id AND co.id = ci.county_id AND ci.name = '{city}' AND st.abbreviation = '{state}';"
            
                with connection.cursor() as cursor:
                    cursor.execute(query)

                    (city_id_count, ) = cursor.fetchone()
                    
                    if (city_id_count == 0):
                        query = f"SELECT co.id AS county_id FROM state st, county co WHERE st.id = co.state_id AND st.abbreviation = '{state}' AND co.name = '{county} County';"
                        cursor.execute(query)

                        (county_id, ) = cursor.fetchone()

                        print(f"INSERT INTO city(name, county_id) VALUES ('{city}', {county_id});")
                    cursor.close()
                
                connection.close()
        except Error as e:
            print(e)
        else:
            connection.close()
    return city_id

county_fips_id = {}
city_ids = {}

with open("data/tx-cities.csv") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        city = row["Town"].title().strip()
        county = row["County"].title().strip()
        
        if (not city in city_ids):
            city_id = find_city_id(city, county, "TX")    
            city_ids[city] = city_id

# with open("data/uscities.csv") as csv_file:
#     reader = csv.DictReader(csv_file)
    
#     i = 1
#     for row in reader:
#         county_fips = row["county_fips"]
#         if (not county_fips in county_fips_id):
#             print(f"Couldn't find {county_fips}")
#         else:
#             city = row["city"]
#             county_id = county_fips_id[county_fips]
#             print(f"INSERT INTO city(id, name, county_id) VALUES ({i}, '{city}', {county_id});")
#             i = i + 1