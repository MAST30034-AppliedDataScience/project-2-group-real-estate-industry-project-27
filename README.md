# Group 27 Real Estate Industry Project

Tutorial Timeslot: Friday 11:00-13:00

## Group Members:
- Callum Sargeant
- Quynh Phoung Le
- Keyue Xie 
- Yuanda Zhu

## Project Resources
### Primary Data Sources:
- Real Estate & Properties for Sale & Rent (2024) Domain. Available at: https://www.domain.com.au/ (Accessed: August-October 2024).
- Department of Families, fairness and housing (2024) Department of Families Fairness and Housing Victoria | Department of Families, Fairness and Housing. Available at: https://www.dffh.vic.gov.au/ (Accessed: August-October 2024).
- Discover and access Victorian Government open data (2024) Datasets - Victorian Government data directory. Available at: https://discover.data.vic.gov.au (Accessed: August-October 2024).
- Victorian State Government (2024) DataShare, Datashare. Available at: https://datashare.maps.vic.gov.au/ (Accessed: August-October 2024). 
### Geospatial Shape Files:
- City of Melbourne Government Data Access API https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/shp
- City of Melbourne Government Data Access API https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/postcodes/exports/geojson
### PTV Data
!!!Keyue to fill in!!!
### Rental Data Scraping:
- Real Estate & Properties for Sale & Rent (2024) Domain.com.au https://www.domain.com.au/rent/melbourne-region-vic/?excludedeposittaken=1&page=1

## Pipeline Instructions:
(Optionally, just run `../notebooks/summary.ipynb` as the first few cells will run all the prerequesite scripts and notebooks before the summary analysis)
- Step 1: run `../scripts/download.py`
- Step 2: run `../notebooks/Data_preprocessing.ipynb`
- Step 3: run `../notebooks/Question1.ipynb`
- Step 4: run `../models/ARIMA model.ipynb`
- Step 5: run `../notebooks/liveability_scoring.ipnb`
- Step 6: run `../notebooks/summary.ipynb`

## Dashboard App Instructions
Ensure that the Shiny and Shinywidgets packages are installed first, then run the following in a command line:
`shiny run --reload --launch-browser ../scripts/app.py`