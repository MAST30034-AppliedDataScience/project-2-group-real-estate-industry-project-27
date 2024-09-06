import requests
import re
from bs4 import BeautifulSoup

def get_soup (url):
    '''Fetch HTML of the page and parse HTML
    Return the parsed HTML'''
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    return soup

def get_price (property):
    '''Find the rental price of the property'''
    price_tag = property.find('p', class_='css-mgq8yx', attrs={'data-testid': 'listing-card-price'})

    # Extract the text content of the <p> tag
    price_text = price_tag.text

    # Use a regular expression to extract the numeric value from the price text
    price_match = re.search(r'\$\d[\d,]*\.?\d*', price_text)
    
    if price_match:
        price_number = price_match.group().replace('$', '').replace(',', '')
        return price_number
    else: 
        return None
    
def get_suburb (property):
    '''Find the suburb and postcode of the property'''
    address_line2 = property.find('span', {'data-testid': 'address-line2'})
    address_details = address_line2.find_all('span')

    if len(address_details) >= 3:
        suburb = address_details[0].text.strip()
        postcode = address_details[2].text.strip()

    return suburb, postcode

def standardize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove the plural 's' (if any) at the end of the word
    text = re.sub(r's$', '', text)
    return text

def get_features (property):
    # Initialize variables for bedrooms and bathrooms
    bedrooms = None
    bathrooms = None
    parkings = None

    # Extract bedrooms and bathrooms
    property_features = property.find_all('span', {'data-testid': 'property-features-text-container'})
    
    for feature in property_features:
        number = feature.contents[0].strip()
        if number == '−':
            number = 0

        label_tag = feature.find('span', {'data-testid': 'property-features-text'})
        if label_tag:
            label = label_tag.text.strip()
            label = standardize_text(label)
        else: continue

        if label == 'bed':
            bedrooms = number
        elif label == 'bath':
            bathrooms = number
        elif label == 'parking':
            parkings = number

    return bedrooms, bathrooms, parkings

def get_next_url (soup):
    page_link_tag = soup.find_all('a', {'data-testid': 'paginator-navigation-button'})
    for link_tag in page_link_tag:
        page_label_tag = link_tag.find('span', class_='css-16q9xmc')
        page_label = page_label_tag.text
        if page_label == 'prev page':
            continue  
        elif page_label == 'next page':
            url = "https://www.domain.com.au" + link_tag['href']
            return url
        else:
            return None
