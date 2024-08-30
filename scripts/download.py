from urllib.request import urlretrieve
import os
import zipfile

# data directory
DATA_DIR = "../data/landing/"

for target_dir in ["geodata"]:
    if not os.path.exists(DATA_DIR + target_dir):
        os.makedirs(DATA_DIR + target_dir)

url_geo_streets = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/street-names/exports/geojson"
url_shape_streets = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/street-names/exports/shp"
GEO_DIR = "geodata/"

print("Begin Street Geospatial Data")

out_dir = DATA_DIR + GEO_DIR + "streets.geojson"
urlretrieve(url_geo_streets, out_dir)

out_dir = DATA_DIR + GEO_DIR + "streets.zip"
urlretrieve(url_shape_streets, out_dir)
with zipfile.ZipFile(out_dir, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR + GEO_DIR)