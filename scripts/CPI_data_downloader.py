from urllib.request import urlretrieve
import os
import zipfile
import pandas as pd

landing_dir = "../data/landing/"
CPI_dir = "cpidata/"

for target_dir in ["inflation"]:
    if not os.path.exists(landing_dir + CPI_dir + target_dir):
        os.makedirs(landing_dir + CPI_dir+ target_dir)

#Consumer Price Index dataset (inflation)
url_cpi = "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jun-quarter-2024/640103.xlsx"

output_dir = landing_dir + CPI_dir + "inflation/" + "CPI_records.xlsx"
urlretrieve(url_cpi, output_dir)

csv_output_dir = landing_dir + CPI_dir + "inflation/" + "CPI_records_sheet2.csv"

cpi_df = pd.read_excel(output_dir, index_col=0, sheet_name = 1)  
cpi_df.to_csv(csv_output_dir, index=False)  