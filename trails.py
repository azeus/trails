import requests
import json
import time

# Define the Overpass and Nominatim API endpoints
overpass_url = "http://overpass-api.de/api/interpreter"
nominatim_url = "https://nominatim.openstreetmap.org/search"


# Function to get the bounding box for a country using Nominatim
def get_bounding_box(country_name):
    try:
        headers = {
            'User-Agent': 'YourAppName (your-email@example.com)'  # Add your own app name and contact information
        }
        params = {
            'q': country_name,
            'format': 'json',
            'limit': 1,
            'polygon_geojson': 0
        }
        response = requests.get(nominatim_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            # Extract the bounding box
            bounding_box = data[0]['boundingbox']
            return [float(bounding_box[0]), float(bounding_box[2]), float(bounding_box[1]), float(bounding_box[3])]
        else:
            print(f"Bounding box not found for {country_name}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounding box for {country_name}: {e}")
        return None


# List of country names (you can add more or use a full list of all countries)
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait",
    "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman",
    "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]
# Initialize an empty list to store all trail names
all_trails = []

# Iterate over each country to get the bounding box and fetch trail names
for country in countries:
    print(f"Fetching bounding box for {country}...")

    # Get the bounding box for the current country
    bbox = get_bounding_box(country)

    if bbox:
        print(f"Bounding box for {country}: {bbox}")

        # Overpass query to get trail names within the country's bounding box
        overpass_query = f"""
        [out:json];
        (
          way["highway"="footway"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
          way["highway"="path"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
          relation["route"="hiking"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out tags;
        """

        try:
            # Send the request to the Overpass API
            response = requests.get(overpass_url, params={'data': overpass_query})
            response.raise_for_status()

            # Parse the response
            data = response.json()

            # Extract trail names and append them to the all_trails list
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    all_trails.append({"name": element['tags']['name'], "country": country})

            print(f"Found {len(data['elements'])} trails in {country}.")

            # Add a delay to avoid overloading the Overpass API (politeness pause)
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching trails for {country}: {e}")
            time.sleep(5)  # Add a delay before continuing to the next country

# Save the combined trail data to a JSON file
if all_trails:
    with open('all_trail_names.json', 'w') as outfile:
        json.dump(all_trails, outfile, indent=2)
    print(f"Successfully saved {len(all_trails)} trail names to 'all_trail_names.json'.")
else:
    print("No trail names were found.")