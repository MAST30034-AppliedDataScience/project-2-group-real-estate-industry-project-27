from urllib.request import urlretrieve
import os
import zipfile

landing_dir = "../data/landing/"
sa2_dir = "sa2data/"

for target_dir in ["population"]:
    if not os.path.exists(landing_dir + sa2_dir + target_dir):
        os.makedirs(landing_dir + sa2_dir+ target_dir)

#Population estimates by SA2, 2001 to 2023, GDA2020, in GeoPackage
url_sa2_population = "https://www.abs.gov.au/statistics/people/population/regional-population/2022-23/32180_ERP_2023_SA2_GDA2020.zip"

output_dir = landing_dir + sa2_dir + "population/" + "sa2_population.zip"
urlretrieve(url_sa2_population, output_dir)
with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(landing_dir + sa2_dir + "population/")