import csv
import re

from mysql.connector import connect, Error
from jproperties import Properties

def find_city_id(city, state, cursor):
    city_id = -1

    query = f"SELECT ci.id as city_id FROM state st, county co, city ci WHERE st.id = co.state_id AND co.id = ci.county_id AND ci.name = '{city}' AND st.abbreviation = '{state}';"
            
    cursor.execute(query)
    row = cursor.fetchone()
    if (row == None):
        print(f"Could not find {city}, {state}.")
    else:
        (city_id, ) = row

    return city_id

def find_address_id(city_id, address_formatted, zip_code, cursor):
    address_id = -1

    if (city_id > 0):
        query = f"SELECT ad.id as address_id FROM city ci, address ad WHERE ci.id = {city_id} AND ci.id = ad.city_id AND ad.address_formatted = '{address_formatted}' AND ad.zip_code = '{zip_code}';"
                
        cursor.execute(query)
        row = cursor.fetchone()
        if (row == None):
            print(f"Could not find {city_id}, {address_formatted}.")
        else:
            (address_id, ) = row

            while (cursor.fetchone()):
                print(f"There was more than one row for {city_id}, {address_formatted}.")

    return address_id

county_fips_id = {}
city_ids = {}
configs = Properties()

with open("data/db.properties", "rb") as config_file:
    configs.load(config_file)
    db_host = configs["DB_HOST"].data
    db_name = configs["DB_NAME"].data
    db_user = configs["DB_USER"].data
    db_pass = configs["DB_PASS"].data

    try:
        with connect(host = db_host, database = db_name, user = db_user, password = db_pass) as connection:
            with connection.cursor() as cursor:
                with open("data/residential.csv") as csv_file:
                    reader = csv.DictReader(csv_file)
                    i = 0
                    for row in reader:
                        i = i + 1
                        state = row["STATE"].strip()
                        city = row["CITY"].title().strip()
                        
                        key = f"{city}-{state}"
                        
                        if (not key in city_ids):
                            percent = i * 100.0 / 44191.0
                            # print(f"We are {percent}% done")
                            city_id = find_city_id(city, state, cursor)
                            city_ids[key] = city_id
                        
                        name = row["OWNER"].title().strip()

                        address_formatted = row["ADDRESS1"].title().strip().replace("'", "''")
                        address_zip = row["ZIP"].strip()
                        
                        find_address_id(city_ids[key], address_formatted, address_zip, cursor)
                cursor.close()    
            connection.close()
    except Error as e:
        print(e)
    else:
        connection.close()
