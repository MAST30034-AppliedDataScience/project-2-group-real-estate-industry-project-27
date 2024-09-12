from urllib.request import urlretrieve
import os
import zipfile

landing_dir = "../data/landing/"
sa2_dir = "sa2data/"

for target_dir in ["boundary"]:
    if not os.path.exists(landing_dir + sa2_dir + target_dir):
        os.makedirs(landing_dir + sa2_dir+ target_dir)

url_sa2_boundary = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip"

output_dir = landing_dir + sa2_dir + "boundary/" + "sa2_boundary.zip"
urlretrieve(url_sa2_boundary, output_dir)
with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(landing_dir + sa2_dir + "boundary/")