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
    print("Crop Guide Information:\n")
    print("Crop Information:")
    crop = input("What crop are you planning to plant?\n")
    crop_description = input("Give a brief description of that crop:\n")
    print("\nGrowing Conditions:")
    soil_conditions = input("What are the soil conditions of the plant?\n")
    temperature_range = input("What are the temperature requirements?\n")
    print("\nClimate & Timing:")
    planting_timing = input("When do you plan to plant the crop?\n")
    print("\nSeed & Variety:")
    seed_type = input("What type of seeds are you using (e.g., heirloom, hybrid)?\n")
    specific_variety = input("Are there any specific varieties you've chosen?\n")
    print("\nPlanting Depth & Spacing:")
    planting_depth = input("How deep should you plant the seeds?\n")
    spacing = input("How much space should there be between plants and rows?\n")
    print("\nWatering & Irrigation:")
    watering_frequency = input("How often do you plan to water the crop?\n")
    irrigation_method = input("What method of irrigation do you intend to use?\n")
    print("\nFertilization:")
    fertilizer_type = input("Do you plan to use fertilizer, and if so, what type?\n")
    fertilization_frequency = input("How often do you plan to fertilize the crop?\n")
    print("\nWeed & Pest Management:")
    weed_management_methods = input("What methods will you use to control weeds?\n")
    pest_diseases = input("Are there any common pests or diseases you need to manage?\n")
    print("\nSupport Structures:")
    support_structures = input("Does this crop require any support structures (e.g., trellises, stakes)?\n")
    print("\nHarvest & Storage:")
    harvest_determination = input("How will you determine when the crop is ready for harvest?\n")
    storage_plans = input("What are your plans for storing the harvested crop?\n")
    # Print the collected information
    print("\nCrop Guide:")
    print("Crop Information:")
    print(f"- Crop: {crop}")
    print("\nGrowing Conditions:")
    print(f"- Soil conditions: {soil_conditions}")
    print("\nClimate & Timing:")
    print(f"- Planting timing: {planting_timing}")
    print("\nSeed & Variety:")
    print(f"- Seed type: {seed_type}")
    print(f"- Specific variety: {specific_variety}")
    print("\nPlanting Depth & Spacing:")
    print(f"- Planting depth: {planting_depth}")
    print(f"- Spacing between plants and rows: {spacing}")
    print("\nWatering & Irrigation:")
    print(f"- Watering frequency: {watering_frequency}")
    print(f"- Irrigation method: {irrigation_method}")
    print("\nFertilization:")
    print(f"- Fertilizer type: {fertilizer_type}")
    print(f"- Fertilization frequency: {fertilization_frequency}")
    print("\nWeed & Pest Management:")
    print(f"- Weed management methods: {weed_management_methods}")
    print(f"- Pests and diseases: {pest_diseases}")
    print("\nSupport Structures:")
    print(f"- Support structures required: {support_structures}")
    print("\nHarvest & Storage:")
    print(f"- Harvest determination method: {harvest_determination}")
    print(f"- Storage plans: {storage_plans}")



class CropGuide:
    def __init__(self, name, cultivation_technique, soil_type, fertilizers, inputs_required, anchorage, estimated_harvest, income_expected):
        """
        Initialize a CropGuide object with the given attributes.

        Parameters:
            name (str): The name of the crop.
            cultivation_technique (str): The technique used for cultivation.
            soil_type (str): The type of soil required for the crop.
            fertilizers (str): The type of fertilizers needed.
            inputs_required (list): List of inputs required for cultivation (e.g., seeds, water, etc.).
            anchorage (str): The anchorage system of the crop.
            estimated_harvest (str): The estimated time for harvest.
            income_expected (str): The expected income from the crop.
        """
        self.name = name
        self.cultivation_technique = cultivation_technique
        self.soil_type = soil_type
        self.fertilizers = fertilizers
        self.inputs_required = inputs_required
        self.anchorage = anchorage
        self.estimated_harvest = estimated_harvest
        self.income_expected = income_expected

    def update_info(self, **kwargs):
        """
        Update the attributes of the CropGuide object.

        Parameters:
            **kwargs: Keyword arguments with attribute names as keys and new values as values.

        Raises:
            AttributeError: If an attribute that does not exist is provided.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'CropGuide' object has no attribute '{key}'")

    def __str__(self):
        """
        Return a string representation of the CropGuide object.
        """
        return (
            f"Crop: {self.name}\n"
            f"Cultivation Technique: {self.cultivation_technique}\n"
            f"Soil Type: {self.soil_type}\n"
            f"Fertilizers: {self.fertilizers}\n"
            f"Inputs Required: {', '.join(self.inputs_required)}\n"
            f"Anchorage: {self.anchorage}\n"
            f"Estimated Harvest: {self.estimated_harvest}\n"
            f"Income Expected: {self.income_expected}"
        )


def main():
    # Create an instance of CropGuide
    crop_guide = CropGuide(
        name="Corn",
        cultivation_technique="Planting in rows",
        soil_type="Loamy soil",
        fertilizers="NPK fertilizer",
        inputs_required=["Seeds", "Water", "Sunlight"],
        anchorage="Strong root system",
        estimated_harvest="4-5 months after planting",
        income_expected="$1000 per acre"
    )

    # Print crop guide information
    print("Crop Guide Information:")
    print(crop_guide)

    # Update crop guide information
    crop_guide.update_info(income_expected="$1200 per acre", soil_type="Sandy loam")

    # Print updated crop guide information
    print("\nUpdated Crop Guide Information:")
    print(crop_guide)


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
