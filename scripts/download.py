from urllib.request import urlretrieve
import os
import zipfile
import pandas as pd
import sys

# data directory
DATA_DIR = "../data/landing/"

for target_dir in ["geodata", "past_rental"]:
    if not os.path.exists(DATA_DIR + target_dir):
        os.makedirs(DATA_DIR + target_dir)

if os.path.exists(DATA_DIR + "_doneflag"):
    sys.exit("Download has already been run, please delete the ../data/landing/_doneflag directory if you need to run the download script again")

url_geo_streets = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/street-names/exports/geojson"
url_shape_streets = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/street-names/exports/shp"

url_geo_suburbs = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/geojson"
url_shape_suburbs = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/shp"
GEO_DIR = "geodata/"

print("Begin Street Geospatial Data")

out_dir = DATA_DIR + GEO_DIR + "streets.geojson"
urlretrieve(url_geo_streets, out_dir)

out_dir = DATA_DIR + GEO_DIR + "streets.zip"
urlretrieve(url_shape_streets, out_dir)
with zipfile.ZipFile(out_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + GEO_DIR)

out_dir = DATA_DIR + GEO_DIR + "suburbs.geojson"
urlretrieve(url_geo_suburbs, out_dir)

out_dir = DATA_DIR + GEO_DIR + "suburbs.zip"
urlretrieve(url_shape_suburbs, out_dir)
with zipfile.ZipFile(out_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + GEO_DIR)


print("Begin Past Rental Data")
url_past_rental = "https://www.dffh.vic.gov.au/moving-annual-rents-suburb-march-quarter-2024-excel"
urlretrieve(url_past_rental, DATA_DIR + "past_rental/" + "moving_rent_suburb.xlsx")

print("Begin Social Indicator Data")
url_social_indicator = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/social-indicators-for-city-of-melbourne-residents-2022/exports/csv?delimiter=%2C"

output_dir = DATA_DIR  + "social_indicator.csv"
urlretrieve(url_social_indicator, output_dir)


print("Begin PTV Data")
ptv_dir = "ptvdata/"

for target_dir in ["train"]:
    if not os.path.exists(DATA_DIR + ptv_dir + target_dir):
        os.makedirs(DATA_DIR + ptv_dir + target_dir)

# This url might be expired, please refer to ../data/README for new url
url_ptv_train = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_4T3RTZ.zip"

output_train_dir = DATA_DIR + ptv_dir + "train/" + "ptv_train.zip"
urlretrieve(url_ptv_train, output_tram_dir)
with zipfile.ZipFile(output_train_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + ptv_dir + "train/")


print("Begin Scraping Domain.com.au")
import run_domain_scraping

# marks if download has finished so that it won't run multiple times
if not os.path.exists(DATA_DIR + "_doneflag"):
        os.makedirs(DATA_DIR + "_doneflag")
