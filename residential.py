import csv
import re
import requests
import json

from mysql.connector import connect, Error
from jproperties import Properties

land_use_map = {
    "100": "1",
    "200": "2",
    "202": "3",
    "203": "4",
    "204": "5",
    "205": "6",
    "300": "7",
    "400": "8",
    "600": "9",
    "1000": "10",
    "1200": "11",
    "1300": "12",
    "1320": "13",
    "1400": "14",
    "1410": "15",
    "2300": "16",
    "2400": "17",
    "3300": "18",
    "7000": "19",
    "7100": "20",
    "7200": "21",
    "7400": "22",
    "7500": "23",
    "7600": "24",
    "7800": "25",
    "7900": "26",
    "8000": "27",
    "8200": "28",
    "8360": "29",
    "8400": "30"
}

assessor_evaluation_map = {
    "8LAW BLDG": "1",
    "COMM BLDG": "2",
    "COMMERCL": "3",
    "EXEMPT": "4",
    "FARM": "5",
    "INDUSTRL": "6",
    "MX U BLDG": "7",
    "RES BLDG": "8",
    "RESIDENTL": "9",
    "TSA BLDG": "10"
}

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
        query = ""
        if (zip_code):
            query = f"SELECT ad.id as address_id FROM city ci, address ad WHERE ci.id = {city_id} AND ci.id = ad.city_id AND ad.address_formatted = '{address_formatted}' AND ad.zip_code = '{zip_code}';"
        else:
            query = f"SELECT ad.id as address_id FROM city ci, address ad WHERE ci.id = {city_id} AND ci.id = ad.city_id AND ad.address_formatted = '{address_formatted}';"
                
        cursor.execute(query)
        row = cursor.fetchone()
        if (row == None):
            if ("LLC" in address_formatted):
                print(f"Address has LLC: {address_formatted}")
            
            # if (zip_code):
            #     print(f"INSERT INTO address (address_formatted, zip_code, city_id) VALUES ('{address_formatted}', '{zip_code}', {city_id});")
            # else:
            #     print(f"INSERT INTO address (address_formatted, city_id) VALUES ('{address_formatted}', {city_id});")
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

def find_zip_code(address, city,state):
    zip_code = None
    url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
    params = {'companyName': '', 'address1': address, 'city': city, 'state': state}
    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, headers=headers, data=params)
    response = json.loads(r.text)
    zip_code = response["addressList"][0]["zip5"]
    
    return zip_code

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

                        owner_id = find_owner_id(owner_name, owner_address_id, cursor)
                        
                        if (owner_id < 0 and owner_address_id > 0):
                            print(f"INSERT INTO owner (name, address_id) VALUES ('{owner_name}', {owner_address_id});")
                        
                        plat_map = row["Map"].strip()
                        lot = row["Lot"].strip()
                        unit = row["Unit"].strip()
                        street_number = row["STREET NUM"].strip()
                        street_name = row["STREET NAME"].title().strip()
                        vision_id = row["VISION ID"].strip()
                        address_formatted = f"{street_number} {street_name}"
                        land_use = row["Land Use Code"]
                        assessor_evaluation = row["ASSESS DESC 1"]
                        actual_year_built = row["ACTUAL YEAR BUILT"]
                        occupancy = row["Occupancy"].strip()
                        ward = row["Ward"]
                        # zip_code = find_zip_code(address_formatted, "Providence", "RI")
                        
                        if (unit):
                            address_formatted = f"{address_formatted}, Unit {unit}"
                        
                        address_id = find_address_id(42, address_formatted, None, cursor)

                        if (not occupancy):
                            occupancy = "NULL"
                        
                        if (owner_id < 0):
                            owner_id = "NULL"
                        
                        query = ""
                        if (address_id > 0):
                            query = (
                                f"UPDATE address SET "
                                f"vision_id = {vision_id}, "
                                f"plat_map = {plat_map}, "
                                f"lot = {lot}, "
                                f"ward = {ward}, "
                                f"actual_year_built = {actual_year_built}, "
                                f"land_use_id = {land_use_map[land_use]}, "
                                f"assessor_evaluation_id = {assessor_evaluation_map[assessor_evaluation]}, "
                                f"occupancy = {occupancy}, "
                                f"owner_id = {owner_id} WHERE address_id = {address_id};"
                            )
                        else:
                            query = (
                                f"INSERT INTO address ("
                                f"street_number, "
                                f"unit, "
                                f"zip_code, "
                                f"address_formatted, "
                                f"city_id, "
                                f"vision_id, "
                                f"plat_map, "
                                f"lot, "
                                f"ward, "
                                f"actual_year_built, "
                                f"land_use_id, "
                                f"assessor_evaluation_id, "
                                f"occupancy, "
                                f"owner_id) VALUES ("
                                f"'{street_number}', "
                                f"'{unit}', "
                                f"NULL, "
                                f"'{address_formatted}', "
                                f"{city_id}, "
                                f"{vision_id}, "
                                f"{plat_map}, "
                                f"{lot}, "
                                f"{ward}, "
                                f"{actual_year_built}, "
                                f"{land_use_map[land_use]}, "
                                f"{assessor_evaluation_map[assessor_evaluation]}, "
                                f"{occupancy}, "
                                f"{owner_id} "
                                f");"
                            )
                        print(query)
                cursor.close()    
            connection.close()
    except Error as e:
        print(e)
    else:
        connection.close()
