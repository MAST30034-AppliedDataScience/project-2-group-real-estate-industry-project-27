# Datasets

# Primary Dataset Sources:
- https://discover.data.vic.gov.au/dataset/social-indicators-for-city-of-melbourne-residents-2022
- https://www.dffh.vic.gov.au/
- https://datashare.maps.vic.gov.au/
- https://www.domain.com.au/

# Ordering PTV Datasets Instructions

## Steps to Order Datasets:

1. Visit the following link to access the respective datasets:
   - **PTV Metro Train Stations**: https://datashare.maps.vic.gov.au/search?md=b6722101-8db5-51f0-8a6f-d1e4fe805b73

2. Add the dataset to the order by clicking **Add to Order**.


3. Once added, **Proceed to Order Configuration**.

4. In the configuration, select the following options:
   - **Projection**: Geographicals on GDA2020
   - **Buffer**: No buffer
   - **Format**: ESRI Shapefile
   - **Area**: Select all available areas.

5. After configuring, **Proceed to MyCart**.

6. Then, **Proceed to Your Details** and enter the required information.

7. Once the order is confirmed, you will receive an email with the URL.  Replace expired URLs in `PTV_data_downloader.py` with the new URLs.


# Requesting a Open Route Service API Key Instructions

## Steps to Requesting a Token:

1. Visit the following link:
   - https://openrouteservice.org/dev/#/login

2. Go to the 'Request a Token' section, select standard for **Token Type**, fill with any random name for **Token Name**

3. Then, click **Create Token**

# Shapefiles and Geojson Data
1. City of Melbourne Government Data Access API https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/shp
2. City of Melbourne Government Data Access API https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/geojson

# Rental Data
1. Real Estate & Properties for Sale & Rent (2024) Domain.com.au
      -> https://www.domain.com.au/rent/melbourne-region-vic/?excludedeposittaken=1&page=1
3. Department of Families, fairness and housing (2024) Department of Families Fairness and Housing Victoria | Department of Families, Fairness and Housing
      -> https://www.dffh.vic.gov.au/
