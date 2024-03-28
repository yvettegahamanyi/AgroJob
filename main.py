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
    print("Registered Farm:")
    print("Owner's Name(s):", owner_names)
    print("Location:", land_location)
    print("Size of Land:", land_size)
    print("Contact Information:", contact_info)
    if additional_info:
        print("Additional Information:", additional_info)

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
        print("\nFound farms in", searchQuery + ":")
        for found_farm in found_farms:
            for key, value in found_farm.items():
                print(key + ":", value)
            print()
    else:
        print("No farms found in", searchQuery)

def crop_guide():
    # Function to display the crop guide
    print("Crop Guide:")
    # Display the crop guide information


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