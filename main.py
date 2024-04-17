#!/usr/bin/python3

import mysql.connector
from prettytable import PrettyTable
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account

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
farm_details = None  

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="AgroJob",
            password="Agro@123Job",
            database="AgroJob",
            port = 3306
        )
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
class BookedFarm:
    def __init__(self, contact_info, province, district, land_size):
        self.province = province
        self.district = district
        self.land_size = land_size
        self.contact_info = contact_info

    def get_province(self):
        return self.province

    def get_district(self):
        return self.district
    
    def get_land_size(self):
        return self.land_size
    
    def get_contact_info(self):
        return self.contact_info
        
def send_email(user, farm_details):
    # Email configurations
    sender_email = user.get_email()
    subject = "Farm Booking Confirmation"
    
    # Customize email message
    message = f"Dear {user.get_name()},\n\nThank you for booking the land!\n\nFarm Details:\nProvince: "
    # {farm_details.get_province()}\nDistrict: {farm_details.get_district()}\nLand Size: {farm_details.get_land_size()}\nContact Information: {farm_details.get_contact_info()}\n\nWe will contact you shortly for further process.\n\nBest regards,\nYour Farm Booking Team"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = "agrojob@reflected-coder-420615.iam.gserviceaccount.com"
    msg['To'] = sender_email
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server and send email
     # Authenticate with OAuth 2.0
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    access_token = credentials.token

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, access_token)
        server.send_message(msg)
    print("Email sent successfully!")

class Farm:
    def __init__(self):
        self.connection = self.connect_to_database()

    def view_available_cultivable_land(connection):

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, province, district, land_size, additional_info, status FROM cultivating_farm")
            rows = cursor.fetchall()

            if not rows:
                print("No cultivable land available.")
                return

            # Create a PrettyTable to display the data in a tabular format
            table = PrettyTable()
            table.field_names = ["ID", "Province", "District", "Size of Land (Hectares)", "Additional Information", "Status"]

            for row in rows:
                table.add_row(row)

            print(table)
        

        except mysql.connector.Error as e:
            print(f"Error fetching data from MySQL database: {e}")

def get_user_by_id(connection, user_id):
    try:
        cursor = connection.cursor(dictionary=True)


        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            # Extract user information from the database
            id = user_data["id"]
            name = user_data["name"]
            email = user_data["email"]
            user_type = user_data["type"]
            
            # Create a User object and return it
            return User(id, name, email, user_type)
        else:
            # User with the provided ID does not exist
            print("User not found.")
            return None
        
    except mysql.connector.Error as e:
        print(f"Error retrieving user data: {e}")
        return None

def view_farm_by_id(connection):
    while True:
        try:
            cursor = connection.cursor()
            farm_id = input("Enter the id to book the farm (or type 'cancel' to cancel): ")
            if farm_id == 'cancel':
                print("Operation cancelled.")
                return
            
            # Check if farm_id is an integer
            if not farm_id.isdigit():
                print("Please enter a valid integer id.")
                continue
            
            # Convert farm_id to integer
            farm_id = int(farm_id)
        
            cursor.execute("SELECT * FROM cultivating_farm WHERE id = %s", (farm_id,))
            farm = cursor.fetchone()
            
            if farm:
                status = farm[7]
                if status == 'booked':
                    print("This farm is already booked.")
                else:
                    global farm_details
                    farm_details = BookedFarm(farm[5], farm[2], farm[3], farm[4])
                    update_query = "UPDATE cultivating_farm SET status = 'booked' WHERE id = %s"
                    cursor.execute(update_query, (farm_id,))
                    connection.commit()
                    # print("Farm booked successfully! Check your email for further process")
                    user = get_user_by_id(connection, farm[1])
                    print(f"Farm booked successfully!\nGoing forward please contact the {user.get_name()}(farm owner) using : ({farm[5]})")

                    break
                print("\n")
            else:
                print("\nFarm not found.\n")

        except pymysql.Error as e:
            print(f"Error fetching data from MySQL database: {e}")

        
def book_farm(connection):

    Farm.view_available_cultivable_land(connection)
    view_farm_by_id(connection)
    # send_email(logged_in_user, farm_details)
        
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
                print(f"\n\nCrop Name: {result['crop_name'].upper()}\n")
                print("Growing Conditions:")
                print(result["growing_conditions"])
                print("\nPlanting & Care:")
                print(result["planting_care"])
                print("\nPest Management:")
                print(result["pest_management"])
                print("\nHarvest & Storage:")
                print(result["harvest_storage"])
                print("\n" + "-" * 80)  # Draw a long line after each crop guide
                # table.add_row([result["crop_name"], result["growing_conditions"], result["planting_care"], result["pest_management"], result["harvest_storage"]])
            # print(table)
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
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM crop_guide")
        rows = cursor.fetchall()

        if not rows:
            print("No crop guides available.")
            return

        # Iterate through each crop guide
        for row in rows:
            print(f"\n\nCrop Name: {row['crop_name'].upper()}\n")
            print("Growing Conditions:")
            print(row["growing_conditions"])
            print("\nPlanting & Care:")
            print(row["planting_care"])
            print("\nPest Management:")
            print(row["pest_management"])
            print("\nHarvest & Storage:")
            print(row["harvest_storage"])
            print("\n" + "-" * 80)  # Draw a long line after each crop guide

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


def mark_cultivable_land(connection):
    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch cultivable lands owned by the logged-in user
        cursor.execute("SELECT id, province, district, land_size, additional_info, status FROM cultivating_farm WHERE owner_id = %s", (logged_in_user.get_id(),))
        rows = cursor.fetchall()

        if not rows:
            print("You have no cultivable land registered.")
            return

        # Display cultivable lands owned by the user in a table
        print("Your cultivable lands:")
        table = PrettyTable()
        table.field_names = ["ID", "Province", "District", "Size of Land (Hectares)", "Additional Information", "Status"]
        for row in rows:
            table.add_row([row["id"], row["province"], row["district"], row["land_size"], row["additional_info"], row["status"]])
        print(table)

        # Ask the user to choose the ID of the cultivable land to update
        while True:
            chosen_id = input("Enter the ID of the cultivable land you want to mark as available/taken (or type 'cancel' to cancel): ").strip().lower()
            if chosen_id == 'cancel':
                print("Operation cancelled.")
                return
            if chosen_id.isdigit():
                chosen_id = int(chosen_id)
                if any(row["id"] == chosen_id for row in rows):
                    break
                else:
                    print("Invalid ID. Please enter a valid ID from the table.")
            else:
                print("Invalid input. Please enter a valid numeric ID.")

        # Ask the user to choose the status
        while True:
            new_status = input("Choose the status (1. available / 2. taken): ").strip()
            if new_status == '1':
                new_status = 'available'
                break
            elif new_status == '2':
                new_status = 'taken'
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        # Update the status of the chosen cultivable land
        update_query = "UPDATE cultivating_farm SET status = %s WHERE id = %s"
        cursor.execute(update_query, (new_status, chosen_id))
        connection.commit()
        print("Cultivable land status updated successfully.")

    except mysql.connector.Error as e:
        print(f"Error updating cultivable land status: {e}")
        
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
                    mark_cultivable_land(connection)
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
                    book_farm(connection)
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
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

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
            create_account(connection)
        elif choice == "8":
            login(connection)
        elif choice == "9":
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