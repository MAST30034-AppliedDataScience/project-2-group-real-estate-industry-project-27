from urllib.request import urlretrieve
import os
import zipfile

landing_dir = "../data/landing/"
ptv_dir = "ptvdata/"

for target_dir in ["tram", "train", "bus"]:
    if not os.path.exists(landing_dir + ptv_dir + target_dir):
        os.makedirs(landing_dir + ptv_dir + target_dir)

# These urls might be expired, please refer to ../data/README for new urls
url_ptv_tram = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_8SMPDX.zip"
url_ptv_train = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_4T3RTZ.zip"
url_ptv_bus = "https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_PMOIMD.zip"


output_tram_dir = landing_dir + ptv_dir + "tram/" + "ptv_tram.zip"
urlretrieve(url_ptv_tram, output_tram_dir)
with zipfile.ZipFile(output_tram_dir, 'r') as zip_ref:
    zip_ref.extractall(landing_dir + ptv_dir + "tram/")

output_train_dir = landing_dir + ptv_dir + "train/" + "ptv_train.zip"
urlretrieve(url_ptv_train, output_tram_dir)
with zipfile.ZipFile(output_train_dir, 'r') as zip_ref:
    zip_ref.extractall(landing_dir + ptv_dir + "train/")

output_bus_dir = landing_dir + ptv_dir + "bus/" + "ptv_bus.zip"
urlretrieve(url_ptv_bus, output_bus_dir)
with zipfile.ZipFile(output_bus_dir, 'r') as zip_ref:
    zip_ref.extractall(landing_dir + ptv_dir + "bus/")

