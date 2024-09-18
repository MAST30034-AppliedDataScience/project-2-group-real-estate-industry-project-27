from urllib.request import urlretrieve
import os
import zipfile

# data directory
DATA_DIR = "../data/landing/"

for target_dir in ["geodata", "past_rental"]:
    if not os.path.exists(DATA_DIR + target_dir):
        os.makedirs(DATA_DIR + target_dir)

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