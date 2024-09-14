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
    
def get_address (property):
    '''Find and return the address, suburb and postcode of the property'''

    # Get address line 1 
    address_line1 = property.find('span', {'data-testid': 'address-line1'})
    address_line1_text = address_line1.get_text().strip().replace(u'\xa0', ' ').rstrip(',')  
    
    # Get suburb and postcode
    address_line2 = property.find('span', {'data-testid': 'address-line2'})
    address_details = address_line2.find_all('span')

    if len(address_details) >= 3:
        suburb = address_details[0].text.strip()
        postcode = address_details[2].text.strip()

    return address_line1_text, suburb, postcode

def standardize_text(text):
    '''Convert text to the same standard'''
    # Convert to lowercase
    text = text.lower()
    # Remove the plural 's' (if any) at the end of the word
    text = re.sub(r's$', '', text)
    return text

def get_features (property):
    '''Find and return number of bedrooms, bathrooms, parking spaces 
    of the property'''
    # Initialize variables for bedrooms, bathrooms and parking spaces
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

def get_available_date(property_soup):
    '''Find and return the day when the property is available to move in'''

    retrieve_day = '12th September 2024'
    summary = property_soup.find('ul', {'data-testid': 'listing-summary-strip'})

    # Check if the property's summary is included in the page
    if summary:
        first_li = summary.find('li')
        first_li_text = first_li.text.strip()

        # Check if available day is included in summary
        if 'Available from' not in first_li_text and 'Date Available:' not in first_li_text:
            return retrieve_day
        
    else: return retrieve_day

    # Get the available day
    available_date = first_li.find('strong').text.strip()   
    if available_date == 'Available Now':
        available_date = retrieve_day  
    else:
        available_date = available_date.split(",")[1].strip()   # get rid of the day of the week
                                                                # only get date, month and year
    return available_date

def get_additional_features(property_soup):
    '''Find additional features of the property and
    return a list of these features'''

    # Initialize the feature list
    additional_features = []

    # Find the additional features on the page
    property_add_features = property_soup.find_all('li', {'data-testid': 
                                                          "listing-details__additional-features-listing"})
    if property_add_features:   # check if website does include any additional features 
        for feature in property_add_features:    
            feature_text = feature.text.strip()
            additional_features.append(feature_text)
    return additional_features

def get_location (property_soup):
    '''Find and return the longitude and latitude of the property's location'''
    property_map = property_soup.find('img', {'class': 'css-12i4cum'})

    if property_map:
        src_link = property_map['src']
        center_match = re.search(r'center=(-?\d+\.\d+,-?\d+\.\d+)', src_link)
    else:
        return None
    
    if center_match:
        center = center_match.group(1)
        return center
    else:
        return None


def get_next_url (soup):
    '''Find and return the url of the next page'''
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
