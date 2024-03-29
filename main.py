#!/usr/bin/python3
registered_farms = []

def view_available_farm_locations():
    # Function to view available farm locations
        print("Available farm locations:")
    # Display the list of available farm locations


def register_farm():
    # Function to register a farm
    # Get the necessary information from the user to register a farm
    
    # Prompt user for full names of the land owner
    owner_names = input('Enter the full names of the land owner: ')

    # Prompt user for the location of the land
    land_location = input('Enter the location of the land: ')

    # Prompt user for the size of the land
    land_size = input('Enter the size of the land (acres, hectares, etc.): ')

    # Prompt user for contact information
    contact_info = input('How can we reach you? Please provide contact details: ')

    # Additional information prompt (optional)
    additional_info = input('Are there any additional details you would like to provide? (Optional): ')

    # Printing the registered farm details
    print("\n\nRegistered Farm:")
    print("Owner's Name(s):", owner_names)
    print("Location:", land_location)
    print("Size of Land:", land_size)
    print("Contact Information:", contact_info)
    if additional_info:
        print("Additional Information:", additional_info, "\n")
    else:
        print("\n\n")
    # Store the registered farm details in a dictionary
    farm_details = {
        "Owner's Name(s)": owner_names,
        "Location": land_location,
        "Size of Land": land_size,
        "Contact Information": contact_info,
        "Additional Information": additional_info if additional_info else "N/A"
    }

 # Append the farm details to the list of registered farms
    registered_farms.append(farm_details)

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
#!/usr/bin/python3
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
# Call the crop_guide function
crop_guide()



def update_crop_guide():
    # Function to update the crop guide
     print('update crop guide:')
    # Get the updated crop guide information from the user


# Menu-driven application
while True:
    print("------ Agrojob Menu ------")
    print("1. View available farm locations")
    print("2. Register a cultivable land")
    print("3. Search for farms in different locations")
    print("4. Crop guide")
    print("5. Update crop guide")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        view_available_farm_locations()
    elif choice == "2":
        register_farm()
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
