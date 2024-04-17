#!/usr/bin/python3

import mysql.connector
from prettytable import PrettyTable

class User:
    def __init__(self, id, name, email, user_type):
        self.id = id
        self.email = email
        self.name = name
        self.user_type = user_type

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def user_type(self):
        return self.user_type
    

logged_in_user = None

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="sql11.freemysqlhosting.net",
            user="sql11698952",
            password="DMwqmetqsW",
            database="sql11698952",
            port = 3306
        )
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
class BookedFarm:
    def __init__(self, owner_names, province, district, land_size, contact_info):
        self.owner_names = owner_names
        self.province = province
        self.district = district
        self.land_size = land_size
        self.contact_info = contact_info
        
def send_email(user, farm):
    # Email configurations
    sender_email = user.get_email()
    subject = "Farm Booking Confirmation"
    
    # Customize email message
    message = f"Dear {user.get_name()},\n\nThank you for booking the land!\n\nFarm Details:\nOwner Name(s): {', '.join(farm.owner_names)}\nProvince: {farm.province}\nDistrict: {farm.district}\nLand Size: {farm.land_size}\nContact Information: {farm.contact_info}\n\nWe will contact you shortly for further process.\n\nBest regards,\nYour Farm Booking Team"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user.get_email()
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        
class Farm:
    def __init__(self):
        self.connection = self.connect_to_database()

    def view_available_cultivable_land(connection):

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cultivating_farm")
            rows = cursor.fetchall()

            if not rows:
                print("No cultivable land available.")
                return

            # Create a PrettyTable to display the data in a tabular format
            table = PrettyTable()
            table.field_names = ["ID", "Owner's Name(s)", "Province", "District", "Size of Land (Hectares)", "Contact Information", "Additional Information"]

            for row in rows:
                table.add_row(row)

            print(table)
        

        except mysql.connector.Error as e:
            print(f"Error fetching data from MySQL database: {e}")
            
            
    def book_farm(connection):

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cultivating_farm")
            rows = cursor.fetchall()

            if not rows:
                print("No cultivable land available.")
                return

            # Create a PrettyTable to display the data in a tabular format
            table = PrettyTable()
            table.field_names = ["ID", "Owner's I(s)", "Province", "District", "Size of Land (Hectares)", "Contact Information", "Additional Information"]

            for row in rows:
                table.add_row(row)

            print(table)
        
        farm_id=input("Enter Farm Id: ")
        

        except mysql.connector.Error as e:
            print(f"Error fetching data from MySQL database: {e}")


    
# Function to register a farm
def register_farm(conn):
    cursor = conn.cursor()
    # create_farm_table(cursor)
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cultivating_farm (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_id INT,
        province VARCHAR(255) NOT NULL,
        district VARCHAR(255) NOT NULL,
        land_size FLOAT NOT NULL,
        contact_info VARCHAR(20) NOT NULL,
        additional_info TEXT,
        status VARCHAR(200) NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES users(id)
    )
    """
    cursor.execute(create_table_query)

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
    INSERT INTO cultivating_farm (owner_id, province, district, land_size, contact_info, additional_info, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    farm_data = (logged_in_user.get_id(), land_province, land_district, float(land_size), contact_info, additional_info, "available")
    cursor.execute(insert_query, farm_data)
    conn.commit()
    print("Registered Farm inserted into the database successfully")

    cursor.close()

def search_farms(connection):
    # Function to search for farms in different locations
    print('Search farms:')
    # Get the keyword input from the user
    search_query = input('Enter the keyword to search farms with location or land size: ')

    # Execute a query to search for farms matching the keyword
    cursor = connection.cursor(dictionary=True)
    search_query = f"%{search_query}%"  # Wildcard search
    select_query = """
    SELECT * FROM cultivating_farm
    WHERE  province LIKE %s OR district LIKE %s OR land_size LIKE %s OR contact_info LIKE %s OR additional_info LIKE %s
    """
    cursor.execute(select_query, (search_query, search_query, search_query, search_query, search_query, search_query))
    found_farms = cursor.fetchall()
    cursor.close()

    if found_farms:
        print("\nFound farms matching the keyword:\n")
        table = PrettyTable()
        table.field_names = ["Province", "District", "Size of Land (Hectares)", "Additional Information", "Status"]
        for found_farm in found_farms:
            table.add_row([found_farm["province"], found_farm["district"], found_farm["land_size"], found_farm["additional_info"],found_farm["status"] ])
        print(table)
    else:
        print("\nNo farms found matching the keyword.\n")

# Function to search crop guide
def search_crop_guide(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        search_query = input("Enter the keyword to search the crop guide: ")

        search_query = f"%{search_query}%"  # Wildcard search

        select_query = """
        SELECT * FROM crop_guide
        WHERE crop_name LIKE %s OR growing_conditions LIKE %s OR planting_care LIKE %s OR pest_management LIKE %s OR harvest_storage LIKE %s
        """
        cursor.execute(select_query, (search_query, search_query, search_query, search_query, search_query))
        results = cursor.fetchall()

        if results:
            print("\nFound matching crop guide:\n")
            table = PrettyTable()
            table.field_names = ["Crop Name", "Growing Conditions", "Planting Care", "Pest Management", "Harvest Storage"]
            for result in results:
                table.add_row([result["crop_name"], result["growing_conditions"], result["planting_care"], result["pest_management"], result["harvest_storage"]])
            print(table)
            print("\n")
        else:
            print("\nNo crop guide found matching the keyword.\n")

    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL database: {e}")

# Function to display the crop guide

def create_crop_guide_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS crop_guide (
        id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(255) UNIQUE,
        growing_conditions TEXT,
        planting_care TEXT,
        pest_management TEXT,
        harvest_storage TEXT
    )
    """
    cursor.execute(create_table_query)
    print("Table 'crop_guide' created successfully")

def crop_guide(conn):
    cursor = conn.cursor()
    create_crop_guide_table(cursor)
    print("Crop Guide Information:\n")

    # Get crop information
    crop_name = input("What crop are you planning to plant? (Crop Name - must be unique)\n")

    # Get growing conditions
    print("\nGrowing Conditions:")
    growing_conditions = input("Describe the ideal growing conditions for this crop:\n")

    # Get planting and care information
    print("\nPlanting & Care:")
    planting_care = input("Provide information on planting depth, spacing, and care instructions:\n")

    # Get pest management information
    print("\nPest Management:")
    pest_management = input("What methods will you use to manage pests and diseases?\n")

    # Get harvest and storage information
    print("\nHarvest & Storage:")
    harvest_storage = input("How will you determine when to harvest the crop and what are your storage plans?\n")

    # Print the collected information
    print("\nCrop Guide:")
    print(f"Crop Name: {crop_name}")
    print("\nGrowing Conditions:")
    print(growing_conditions)
    print("\nPlanting & Care:")
    print(planting_care)
    print("\nPest Management:")
    print(pest_management)
    print("\nHarvest & Storage:")
    print(harvest_storage)

    # Insert crop guide information into the database
    insert_query = """
    INSERT INTO crop_guide (crop_name, growing_conditions, planting_care, pest_management, harvest_storage)
    VALUES (%s, %s, %s, %s, %s)
    """
    crop_guide_data = (crop_name, growing_conditions, planting_care, pest_management, harvest_storage)
    cursor.execute(insert_query, crop_guide_data)
    conn.commit()
    print("Crop Guide inserted into the database successfully")


def view_crop_guides(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crop_guide")
        rows = cursor.fetchall()

        if not rows:
            print("No crop guides available.")
            return

        # Create a PrettyTable to display the data in a tabular format
        table = PrettyTable()
        table.field_names = ["ID", "Crop Name", "Growing conditions", "Planting Care", "Pest Management", "Harvest Storage"]

        for row in rows:
            table.add_row(row)

        print(table)

    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL database: {e}")

def update_crop_guide(conn, crop_name):
    cursor = conn.cursor()
    # cursor.execute()

    # Check if the crop exists in the database
    cursor.execute("SELECT * FROM crop_guide WHERE crop_name=%s", (crop_name,))
    existing_crop = cursor.fetchone()

    if existing_crop:
        print(f"Updating information for {crop_name}:\n")
        # Get growing conditions
        growing_conditions = input("Describe the ideal growing conditions for this crop:\n")

        # Get planting and care information
        planting_care = input("Provide information on planting depth, spacing, and care instructions:\n")

        # Get pest management information
        pest_management = input("What methods will you use to manage pests and diseases?\n")

        # Get harvest and storage information
        harvest_storage = input("How will you determine when to harvest the crop and what are your storage plans?\n")

        # Update information in the database
        cursor.execute("UPDATE crop_guide SET growing_conditions=%s, planting_care=%s, pest_management=%s, harvest_storage=%s WHERE crop_name=%s",
                       (growing_conditions, planting_care, pest_management, harvest_storage, crop_name))
        conn.commit()

        print("\nCrop guide updated successfully!")
    else:
        print(f"Error: {crop_name} does not exist in the crop guide.")
        
def create_account(connection):
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        type ENUM('farmOwner', 'farmTenant') NOT NULL
    )
    """
    cursor.execute(create_table_query)
    
    print("------ Create Account ------")
    name = input("Enter your name: ")
    email = input("Enter a Email: ")
    password = input("Enter a password: ")

    # Prompt user to choose user type
    print("Select your type:")
    print("1. Farm Owner")
    print("2. Farm Tenant")
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        user_type = "farmOwner"
    elif choice == "2":
        user_type = "farmTenant"
    else:
        print("Invalid choice. Please select 1 or 2.")
        return

    # Check if the email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Email already exists. Please choose a different email.")
        return

    # Insert new user into the database
    insert_query = "INSERT INTO users (name, email, password, type) VALUES (%s, %s, %s, %s)"
    user_data = (name, email, password, user_type)
    cursor.execute(insert_query, user_data)
    connection.commit()
    print("Account created successfully.")

def login(connection):
    cursor = connection.cursor()
    print("------ Login ------")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Check if the email and password match
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    global logged_in_user
    if user:
        print("Login successful.")
        logged_in_user = User( user[0], user[1], user[2], user[4])
        loggedIn 
        user_type = user[4]  # Assuming user type is stored in the fifth column
        if user_type == "farmOwner":
            print("Welcome, Farm Owner!")
            while True:
                print("------ Farm Owner Menu ------")
                print("1. Register cultivable land")
                print("2. Mark cultivable land as available or taken")
                print("3. Log out")
                
                owner_choice = input("Enter your choice (1-4): ")
                
                if owner_choice == "1":
                    register_farm(connection)
                elif owner_choice == "2":
                    mark_cultivable_land()
                elif owner_choice == "3":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please enter a number from 1 to 3.")

        elif user_type == "farmTenant":
            print("Welcome, Farm Tenant!")
            while True:
                print("------ Farm Tenant Menu ------")
                print("1. Book cultivable land")
                print("2. Log out")
                
                tenant_choice = input("Enter your choice (1-2): ")
                
                if tenant_choice == "1":
                    book_cultivable_land()
                elif tenant_choice == "2":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please enter a number from 1 to 2.")

        else:
            print("Invalid user type.")
    else:
        print("Invalid email or password.")

    cursor.close()

def delete_table_cultivating_farm(connection):
    try:
        cursor = connection.cursor()
        # SQL query to drop the table
        drop_table_query = "DROP TABLE IF EXISTS cultivating_farm"
        cursor.execute(drop_table_query)
        connection.commit()
        print("Table 'cultivating_farm' deleted successfully")
    except mysql.connector.Error as e:
        print(f"Error deleting table: {e}")
        
def main():
    # Establish database connection
    connection = connect_to_database()
    if not connection:
        return


    # Menu-driven application
    while True:
        print("------ AgroJob Menu ------")
        print("1. View available cultivable land")
        print("2. Search for farms in different locations")
        print("3. Create Crop guide")
        print("4. View all crop guides")
        print("5. Update crop guide")
        print("6. Search crop guide")
        print("7. Create an Account")
        print("8. Login to AgroJob") 
        # Check user type and add booking option for farmTenants
        if logged_in_user.get_user_type() == "farmTenant":
            print("9. Book a farm")
        print("10. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
           Farm.view_available_cultivable_land(connection)
        elif choice == "2":
            search_farms(connection)
        elif choice == "3":
            crop_guide(connection)
        elif choice == "4":
            view_crop_guides(connection)
        elif choice == "5":
            crop_name=input("Enter crop name: ")
            update_crop_guide(connection,crop_name)
        elif choice == "6":
            search_crop_guide(connection)
        elif choice == "7":
            delete_table_cultivating_farm(connection)
        elif choice == "8":
            login(connection)
        elif choice == "9":
            book_farm(connection)
        elif choice == "10":
            print("Exiting the application...")
            feedback = input("Did you enjoy using the program? (yes/no): ").lower()
            if feedback == "yes":
                improvement = input("Are there any improvements you'd like to suggest? (yes/no): ").lower()
                if improvement == "yes":
                    print("Thank you for your feedback! Please enter your suggestions below:")
                    user_suggestion = input()
                    print("Thanks for your inputs. We appreciate your suggestions!")
            elif feedback == "no":
                improvement = input("What can we do to improve the system for a better experience next time? ")
                print("Thank you for your feedback. We'll work on improving the system.")
            else:
                print("Invalid response. Exiting the program without feedback.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")
            

    # Close database connection when exiting the program
    connection.close()

# Ensure main function is called
if __name__ == "__main__":
    main()