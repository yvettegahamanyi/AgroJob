#!/usr/bin/python3

import mysql.connector
registered_farms = []

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="sql6.freemysqlhosting.net",
            user="sql6695184",
            password="xNWAebcl1q",
            database="sql6695184",
            port = 3306
        )
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def view_available_farm_locations():
    # Function to view available farm locations
        print("Available farm locations:")
    # Display the list of available farm locations


def create_farm_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cultivating_farm (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_names VARCHAR(255) NOT NULL,
        province VARCHAR(255) NOT NULL,
        district VARCHAR(255) NOT NULL,
        land_size FLOAT NOT NULL,
        contact_info VARCHAR(20) NOT NULL,
        additional_info TEXT
    )
    """
    cursor.execute(create_table_query)
    print("Table 'cultivating_farm' created successfully")

# Function to register a farm
def register_farm(conn):
    cursor = conn.cursor()
    create_farm_table(cursor)

    # Prompt user for full names of the land owner
    while True:
        owner_names = input('Enter the full names of the land owner (at least 2 names): ').strip()
        if len(owner_names.split()) >= 2 and all(name.isalpha() for name in owner_names.split()):
            break
        else:
            print("Please enter at least 2 names (alphabetical characters only).")

    # Dictionary of provinces and corresponding districts
    province_districts = {
        "Kigali": ["Nyarugenge", "Kicukiro", "Gasabo"],
        "Eastern Province": ["Kirehe", "Bugesera", "Ngoma"],
        "Western Province": ["Karongi", "Nyamasheke", "Rutsiro"]
    }

    # Prompt user for the province of the location of the land (multiple choice)
    print("Choose the province of the location of the land:")
    for i, province in enumerate(province_districts.keys(), 1):
        print(f"{i}. {province}")
    province_choice = int(input("Enter the number corresponding to the province: "))
    land_province = list(province_districts.keys())[province_choice - 1]

    # Prompt user for the district of the location of the land (based on province selection)
    print("Choose the district of the location of the land:")
    districts = province_districts[land_province]
    for i, district in enumerate(districts, 1):
        print(f"{i}. {district}")
    district_choice = int(input("Enter the number corresponding to the district: "))
    land_district = districts[district_choice - 1]

    # Prompt user for the size of the land in hectares
    while True:
        land_size = input('Enter the size of the land (in hectares): ').strip()
        if land_size.replace('.', '').isdigit():
            break
        else:
            print("Please enter a valid numeric value for land size.")

    # Prompt user for contact information
    while True:
        contact_info = input('Enter the contact information (10-digit phone number starting with 07): ').strip()
        if len(contact_info) == 10 and contact_info.startswith("07") and contact_info[2:].isdigit():
            break
        else:
            print("Please enter a valid 10-digit phone number starting with 07.")

    # Additional information prompt (optional)
    additional_info = input('Enter any additional information (Optional): ').strip()

    # Insert farm details into the database
    insert_query = """
    INSERT INTO cultivating_farm (owner_names, province, district, land_size, contact_info, additional_info)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    farm_data = (owner_names, land_province, land_district, float(land_size), contact_info, additional_info)
    cursor.execute(insert_query, farm_data)
    conn.commit()
    print("Registered Farm inserted into the database successfully")

    cursor.close()

def search_farms():
    # Function to search for farms in different locations
    print('Search farms:')
    # Get the location input from the user and display the matching farms
    # Get the location input from the user
    searchQuery = input('Enter the keyword to search farms with location or land size: ')
    found_farms = []
    for farm in registered_farms:
        if farm["Location"].lower() == searchQuery.lower() or farm["Size of Land"].lower() == searchQuery.lower():
            found_farms.append(farm)
    
    if found_farms:
        print("\nFound farms in", searchQuery + ":\n\n")
        for found_farm in found_farms:
            for key, value in found_farm.items():
                print(key + ":", value)
            print("\n")
    else:
        print("\n\nNo farms found in", searchQuery,"\n")

def crop_guide():
    # Function to display the crop guide
    print("Crop Guide:")
    # Display the crop guide information


def update_crop_guide():
    # Function to update the crop guide
     print('update crop guide:')
    # Get the updated crop guide information from the user

def main():
    # Establish database connection
    connection = connect_to_database()
    if not connection:
        return
    
    
    # Menu-driven application
    while True:
        print("------ Agrojob Menu ------")
        print("1. View available cultivable land")
        print("2. Register a cultivable land")
        print("3. Search for farms in different locations")
        print("4. Crop guide")
        print("5. Update crop guide")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            view_available_farm_locations()
        elif choice == "2":
            register_farm(connection)
        elif choice == "3":
            search_farms()
        elif choice == "4":
            crop_guide()
        elif choice == "5":
            update_crop_guide()
        elif choice == "6":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

    # Close database connection when exiting the program
    connection.close()

# Ensure main function is called
if __name__ == "__main__":
    main()
