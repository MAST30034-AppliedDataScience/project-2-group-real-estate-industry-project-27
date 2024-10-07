from urllib.request import urlretrieve
import os


landing_dir = "../data/landing/"

url_social_indicator = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/social-indicators-for-city-of-melbourne-residents-2022/exports/csv?delimiter=%2C"

output_dir = landing_dir  + "social_indicator.csv"
urlretrieve(url_social_indicator, output_dir)

