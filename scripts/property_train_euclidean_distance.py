import pandas as pd
import geopandas as gpd
import numpy as np

train_station_gpd = gpd.read_file("../data/landing/ptvdata/train/ll_gda2020/esrishape/whole_of_dataset/victoria/PTV/PTV_METRO_TRAIN_STATION.shp")
property_df = pd.read_csv("../data/raw/property_w_coordinates.csv")

# Function to calculate Euclidean distance between two points (lat, lon)
def euclidean_dist(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

property_df['min_train_dist'] = np.nan
property_df['closest_train_station'] = ""

for index, property_row in property_df.iterrows():
    lat1, lon1 = property_row['latitude'], property_row['longitude']
    
    # Calculate distances from one property to all train stations
    train_station_gpd['distance'] = train_station_gpd.apply(
        lambda row: euclidean_dist(lat1, lon1, row['LATITUDE'], row['LONGITUDE']),
        axis=1
    )
    
    # Find the minimum distance
    min_distance_station = train_station_gpd.loc[train_station_gpd['distance'].idxmin()]
    
    
    property_df.at[index, 'min_train_dist'] = min_distance_station['distance']
    property_df.at[index, 'closest_train_station'] = min_distance_station['STOP_NAME']

property_df.to_csv("../data/curated/processed property_w_distance.csv", index=False)
