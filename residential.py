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
            if ("LLC" in address_formatted):
                print(f"Address has LLC: {address_formatted}")
            
            print(f"INSERT INTO address (address_formatted, zip_code, city_id) VALUES ('{address_formatted}', '{zip_code}', {city_id});")
        else:
            (address_id, ) = row

            while (cursor.fetchone()):
                print(f"There was more than one row for {city_id}, {address_formatted}.")

    return address_id

def find_owner_id(owner_name, address_id, cursor):
    owner_id = -1

    if (address_id > 0):
        query = f"SELECT id as owner_id FROM owner WHERE name = '{owner_name}' AND address_id = {address_id};"

        cursor.execute(query)
        row = cursor.fetchone()
        if (row == None):
            print(f"Could not find {owner_name}")
        else:
            (owner_id, ) = row

            while (cursor.fetchone()):
                print(f"There was more than one row for {owner_name}, {address_id}.")
    return owner_id

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
                        owner_state = row["STATE"].strip()
                        owner_city = row["CITY"].title().strip()
                        
                        key = f"{owner_city}-{owner_state}"
                        
                        if (not key in city_ids):
                            city_id = find_city_id(owner_city, owner_state, cursor)
                            city_ids[key] = city_id
                        
                        owner_name = row["OWNER"].title().strip()

                        owner_address_formatted = row["ADDRESS1"].title().strip().replace("'", "''")
                        owner_address_zip = row["ZIP"].strip()
                        owner_address_zip_4 = ""
                        
                        if (re.match(r"[0-9]{5}-[0-9]{4}", owner_address_zip)):
                            zips = owner_address_zip.split("-")
                            owner_address_zip = zips[0]
                            owner_address_zip_4 = zips[1]
                        elif (re.match(r"[0-9]{5}[0-9]{4}", owner_address_zip)):
                            owner_address_zip_4 = owner_address_zip[-4:]
                            owner_address_zip = owner_address_zip[0:5]
                        
                        owner_address_id = find_address_id(city_ids[key], owner_address_formatted, owner_address_zip, cursor)

                        if (owner_address_id):
                            print(f"INSERT INTO owner (name, address_id) VALUES ('{owner_name}', {owner_address_id});")
                cursor.close()    
            connection.close()
    except Error as e:
        print(e)
    else:
        connection.close()
