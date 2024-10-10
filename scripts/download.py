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
url_past_rental = "https://www.dffh.vic.gov.au/moving-annual-rents-suburb-march-quarter-2023-excel"
urlretrieve(url_past_rental, DATA_DIR + "past_rental/" + "moving_rent_suburb.xlsx")

print("Begin Social Indicator Data")
url_social_indicator = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/social-indicators-for-city-of-melbourne-residents-2022/exports/csv?delimiter=%2C"

output_dir = DATA_DIR  + "social_indicator.csv"
urlretrieve(url_social_indicator, output_dir)

print("Begin SA2 Data")
sa2_dir = "sa2data/"

for target_dir in ["boundary"]:
    if not os.path.exists(DATA_DIR + sa2_dir + target_dir):
        os.makedirs(DATA_DIR + sa2_dir+ target_dir)

url_sa2_boundary = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip"

output_dir = DATA_DIR + sa2_dir + "boundary/" + "sa2_boundary.zip"
urlretrieve(url_sa2_boundary, output_dir)
with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + sa2_dir + "boundary/")

for target_dir in ["population"]:
    if not os.path.exists(DATA_DIR + sa2_dir + target_dir):
        os.makedirs(DATA_DIR + sa2_dir+ target_dir)

#Population estimates by SA2, 2001 to 2023, GDA2020, in GeoPackage
url_sa2_population = "https://www.abs.gov.au/statistics/people/population/regional-population/2022-23/32180_ERP_2023_SA2_GDA2020.zip"

output_dir = DATA_DIR + sa2_dir + "population/" + "sa2_population.zip"
urlretrieve(url_sa2_population, output_dir)
with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + sa2_dir + "population/")

print("Begin CPI data")
CPI_dir = "cpidata/"

for target_dir in ["inflation"]:
    if not os.path.exists(DATA_DIR + CPI_dir + target_dir):
        os.makedirs(DATA_DIR + CPI_dir+ target_dir)

#Consumer Price Index dataset (inflation)
url_cpi = "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jun-quarter-2024/640103.xlsx"

output_dir = DATA_DIR + CPI_dir + "inflation/" + "CPI_records.xlsx"
urlretrieve(url_cpi, output_dir)

csv_output_dir = DATA_DIR + CPI_dir + "inflation/" + "CPI_records_sheet2.csv"

cpi_df = pd.read_excel(output_dir, index_col=0, sheet_name = 1)  
cpi_df.to_csv(csv_output_dir, index=False)  

print("Begin PTV Data")
ptv_dir = "ptvdata/"

for target_dir in ["tram", "train", "bus"]:
    if not os.path.exists(DATA_DIR + ptv_dir + target_dir):
        os.makedirs(DATA_DIR + ptv_dir + target_dir)

# These urls might be expired, please refer to ../data/README for new urls
url_ptv_tram = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_8SMPDX.zip"
url_ptv_train = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_4T3RTZ.zip"
url_ptv_bus = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_PMOIMD.zip"


output_tram_dir = DATA_DIR + ptv_dir + "tram/" + "ptv_tram.zip"
urlretrieve(url_ptv_tram, output_tram_dir)
with zipfile.ZipFile(output_tram_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + ptv_dir + "tram/")

output_train_dir = DATA_DIR + ptv_dir + "train/" + "ptv_train.zip"
urlretrieve(url_ptv_train, output_tram_dir)
with zipfile.ZipFile(output_train_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + ptv_dir + "train/")

output_bus_dir = DATA_DIR + ptv_dir + "bus/" + "ptv_bus.zip"
urlretrieve(url_ptv_bus, output_bus_dir)
with zipfile.ZipFile(output_bus_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + ptv_dir + "bus/")

print("Begin Scraping Domain.com.au")
import run_domain_scraping

# marks if download has finished so that it won't run multiple times
if not os.path.exists(DATA_DIR + "_doneflag"):
        os.makedirs(DATA_DIR + "_doneflag")