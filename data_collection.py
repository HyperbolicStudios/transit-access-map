import datetime as dt
import os
from inspect import getsourcefile
from os.path import abspath
import json
import traceback

import pandas as pd
import googlemaps
import geopandas as gpd

#set active directory to file location
directory = abspath(getsourcefile(lambda:0))
#check if system uses forward or backslashes for writing directories
if(directory.rfind("/") != -1):
    newDirectory = directory[:(directory.rfind("/")+1)]
else:
    newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

gmaps = googlemaps.Client(os.environ["Google_Cloud_Credentials"])
arrival_time=dt.datetime(2022, 11, 8, 8, 30) #arrive at 8:30AM on sept 7, 2022 (weekday, non-holiday schedule)

def dump(result):
    with open('json_data.json', 'w') as outfile:
        json.dump(result[0], outfile)
    return

def get_travel_time(start_point, destination, mode):
    try:
        result = gmaps.directions(start_point,
                                    destination,
                                    mode=mode,
                                    arrival_time=arrival_time)
#    print(result)

        if mode == "transit":
            duration = (arrival_time.timestamp()-result[0]["legs"][0]["departure_time"]["value"])/60.0

        if mode == "bicycling":
            duration = result[0]["legs"][0]["duration"]["value"]/60.0

        if mode == "driving":
            duration = result[0]["legs"][0]["duration"]["value"]
            departure_time = arrival_time-dt.timedelta(seconds=duration)
            new_result = gmaps.directions(start_point,
                                         destination,
                                         mode="driving",
                                         departure_time=departure_time)

            duration = new_result[0]["legs"][0]["duration_in_traffic"]["value"]/60

        #print("{}: {}".format(mode,val))
        return(duration)
    except:
    #    traceback.print_exc()
        return("???")


def collect_data():
    df = gpd.read_file('vancouver.geojson')
    df = df.to_crs('EPSG:4326')
    df["center"] = df.centroid

    destination = "University of British Columbia, Vancouver"

    for index in range(2748,len(df)):
        print("{}/{}".format(index+1,len(df)))

        coords = (df.loc[index,'center'].y,df.loc[index,'center'].x)
        df.loc[index,'Transit Time'] = get_travel_time(coords, destination, "transit")
        df.loc[index,'Car Time'] = get_travel_time(coords, destination, "driving")
        df.loc[index,'Bike Time'] = get_travel_time(coords, destination, "bicycling")

        df.to_csv("data/UBC Data.csv",index=False)

    """
    destination = "Downtown Vancouver"

    for index in df.index:
        print("{}/581".format(index+1))
    #if pd.isnull(df.loc[index, "Bike Time"]) == True:
        coords = (df.loc[index,'Y'],df.loc[index,'X']) #latitude, longitude order
        df.loc[index,'Transit Time'] = get_travel_time(coords, destination, "transit")
        df.loc[index,'Car Time'] = get_travel_time(coords, destination, "driving")
        df.loc[index,'Bike Time'] = get_travel_time(coords, destination, "bicycling")

        df.to_csv("data/Downtown Vancouver Data.csv")
        """
    return

#collect_data()
df = gpd.read_file('vancouver.geojson')
df = df.to_crs('EPSG:4326')
print(df.columns)
df = df.drop(['geometry'],axis=1)
df.to_csv("master.csv")
