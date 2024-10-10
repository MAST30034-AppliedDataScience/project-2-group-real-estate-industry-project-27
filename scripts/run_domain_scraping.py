import pandas as pd

import scrape_domain

# Initialise the first page of property listings
url = "https://www.domain.com.au/rent/melbourne-region-vic/?excludedeposittaken=1&page=1"
properties = []
page_count = 1

while url:  # stop when there are no more pages to scrape
    print("Begin page", page_count)    

    # Fetch and parse HTML of the current page
    soup = get_soup(url)    # function from scrape domain.com

    # Get a list of all property listings on the page
    listings = soup.find_all('div', {'class': 'css-qrqvvg'})

    # Extract information of each property
    for property in listings:
        price = get_price(property)
        if not price:   # exclude properties that do not have a rental price         
            continue     # usually are properties under application

        address_line1, suburb, postcode = get_address(property)
        bedrooms, bathrooms, parkings = get_features(property)
        property_type = property.find('span', class_='css-693528').text.strip()     

        # Look into the property's page to find additional features
        link = property.find('a', href = True)
        property_url = link['href']
        property_soup = get_soup(property_url)

        additional_features = get_additional_features(property_soup)
        
        # Store the extracted data in a dictionary
        property_data = {
            'price (AUD per week)': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'parkings': parkings,
            'property type': property_type,
            'address': address_line1,
            'suburb': suburb,
            'postcode': postcode,
            'additional features': additional_features,
            'property url': property_url
        }

        # Append the dictionary to the list of properties
        properties.append(property_data)
    url = get_next_url(soup)
    page_count += 1

# Convert list of dictionaries to a pandas DataFrame
df = pd.DataFrame(properties)

# Write the DataFrame to a CSV file
df.to_csv('../data/landing/properties.csv', index=False)

print('Data successfully written to properties.csv')