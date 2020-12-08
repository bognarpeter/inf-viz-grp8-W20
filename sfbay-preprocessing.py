import numpy as np
import pandas as pd
import os
from datetime import datetime as dt

dt.now().replace(microsecond=0).isoformat()

R_MAJOR = 6378137.000
DATA_PATH = "data"
sfbay_data = "SFBay.csv"
location_data = "StationLocations.csv"
sfbay_final_data = "sfbay_final.csv"


def get_time():
    return dt.now().replace(microsecond=0).isoformat()


def to_mercators(lat, lon):
    """
    Define function to switch from lat/long to mercator coordinates
    """
    x = R_MAJOR * np.radians(lon)
    scale = x / lon
    y = (
        180.0
        / np.pi
        * np.log(np.tan(np.pi / 4.0 + lat * (np.pi / 180.0) / 2.0))
        * scale
    )
    return (x, y)


# Read in data
sfbay_data_path = os.path.join(DATA_PATH, sfbay_data)
location_data_path = os.path.join(DATA_PATH, location_data)

print(
    f"[{get_time()}] Starts to process data using [{sfbay_data_path}, {location_data_path}]"
)

sfbay = pd.read_csv(sfbay_data_path, delimiter=";")
locations = pd.read_csv(location_data_path, index_col=False)


#                            #
# Pre-process Locations data #
#                            #

del locations["Comments"]
#
# stat_num: Station Number
# lat_deg: North Latitude Degrees
# lat_min: North Latitude Minutes
# lon_deg: West Longitude Degrees
# lon_min: West Longitude Minutes
#
locations_header = ["stat_num", "lat_deg", "lat_min", "lon_deg", "lon_min"]
locations.columns = locations_header

# remove minute sign (') and cast to proper types
locations["lat_min"] = locations["lat_min"].str.replace(r"'$", "")
locations["lon_min"] = locations["lon_min"].str.replace(r"'$", "")
locations = locations.astype("float64")
locations["stat_num"] = locations["stat_num"].astype("int32")

# convert minutes to degrees and sum values
locations["lat"] = locations["lat_deg"] + locations["lat_min"] / 60
locations["lon"] = locations["lon_deg"] - locations["lon_min"] / 60

# drop unnecesary columns
columns_to_drop = [col for col in locations_header if col != "stat_num"]
locations = locations.drop(columns_to_drop, axis=1)

# Obtain list of mercator coordinates
mercators = [
    to_mercators(x, y) for x, y in list(zip(locations["lat"], locations["lon"]))
]

# Create mercator column in our df
locations["mercator"] = mercators
# Split that column out into two separate columns - mercator_x and mercator_y
locations[["mercator_x", "mercator_y"]] = locations["mercator"].apply(pd.Series)
locations = locations.drop(columns=["mercator"])


#                        #
# Pre-process SFBay data #
#                        #

sfbay.rename(columns={"Station.Number": "stat_num"}, inplace=True)
sfbay["stat_num"] = sfbay["stat_num"].astype("int32")

# sfbay_final = pd.concat([sfbay, locations], axis=1, join='inner')
sfbay_final = sfbay.merge(
    locations, on="stat_num", how="inner"
)  # , suffixes=('_1', '_2'))

sfbay_final_data_path = os.path.join(DATA_PATH, sfbay_final_data)
sfbay_final.to_csv(sfbay_final_data_path, sep=",")

print(f"[{get_time()}] Data has been processed and saved: {sfbay_final_data_path}")
