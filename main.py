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
                with open("data/owners.csv") as csv_file:
                    reader = csv.DictReader(csv_file)
                    i = 0
                    for row in reader:
                        i = i + 1
                        state = row["OWNER_STATE"].strip()
                        city = row["OWNER_CITY"].title().strip()
                        
                        key = f"{city}-{state}"
                        
                        if (not key in city_ids):
                            percent = i * 100.0 / 44191.0
                            # print(f"We are {percent}% done")
                            city_id = find_city_id(city, state, cursor)
                            city_ids[key] = city_id
                        
                        first_name = row["OWNER_FIRST_NAME"].title().strip()
                        last_name = row["OWNER_LAST_NAME"].title().strip()
                        company_name = row["OWNER_COMPANY"].title().strip()
                        address_formatted = row["OWNER_FORMATTED_ADDRESS"].title().strip().replace("'", "''")
                        address_number = row["OWNER_NUMBER"].strip()
                        address_street = row["OWNER_STREET"].title().replace("'", "''").strip()
                        address_suffix = row["OWNER_SUFFIX"].title().strip()
                        address_unit = row["OWNER_UNIT"].strip()
                        address_zip = row["OWNER_ZIP"].strip()
                        address_zip_4 = ""
                        if (re.match(r"[0-9]{5}-[0-9]{4}", address_zip)):
                            zips = address_zip.split("-")
                            address_zip = zips[0]
                            address_zip_4 = zips[1]
                        
                        find_address_id(city_ids[key], address_formatted, address_zip, cursor)
                cursor.close()    
            connection.close()
    except Error as e:
        print(e)
    else:
        connection.close()

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