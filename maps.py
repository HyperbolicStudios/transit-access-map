import googlemaps
import datetime
import os
from inspect import getsourcefile
from os.path import abspath
import json
import pandas as pd
#from graphing import graph_variables
#set active directory to file location
directory = abspath(getsourcefile(lambda:0))
#check if system uses forward or backslashes for writing directories
if(directory.rfind("/") != -1):
    newDirectory = directory[:(directory.rfind("/")+1)]
else:
    newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

gmaps = googlemaps.Client(os.environ["Google_Cloud_Credentials"])
arrival_time=datetime.datetime(2022, 6, 21,8,30)

def get_travel_time(start_point=(48.417927,-123.316363),mode="transit"):
    #Look up an address with reverse geocoding
    # Request directions via public transit

    result = gmaps.directions(start_point,
                                         "UVic Exchange, Saanich, BC",
                                         mode=mode,
                                         arrival_time=arrival_time)
#    print(result)
    #with open('json_data.json', 'w') as outfile:
    #    json.dump(result[0], outfile)

    """
    with open('json_data.json') as json_file:
        data = json.load(json_file)
    """

    try:
        return(result[0]["legs"][0]["departure_time"]["value"])
    except:
        try:
            duration = result[0]["legs"][0]["duration"]["value"]
            return((arrival_time-datetime.timedelta(seconds=duration)).timestamp())
        except:
            return("???")

def time_in_traffic(start_point,departure_time):
    result = gmaps.directions(start_point,
                                 "UVic Exchange, Saanich, BC",
                                 mode="driving",
                                 departure_time=departure_time)


    duration = result[0]["legs"][0]["duration_in_traffic"]["value"]
    return((arrival_time-datetime.timedelta(seconds=duration)).timestamp())


def map():
    df = pd.read_csv("output/output.csv")
    for index in df.index:
        if pd.isnull(df.loc[index, "Bike Time"]) == True:
            coords = (df.loc[index,'Y'],df.loc[index,'X']) #latitude, longitude order
            print(coords)
            #df.loc[index,'Transit Time'] = get_travel_time(coords,"transit")
            #df.loc[index,'Car Time'] = get_travel_time(coords,"driving")
            df.loc[index,'Bike Time'] = get_travel_time(coords,"bicycling")
            df.to_csv("output/output.csv")
    return

df = pd.read_csv("output/output.csv")
for index in df.index:
    coords = (df.loc[index,'Y'],df.loc[index,'X'])
    print(coords)
    departure_time = datetime.datetime.fromtimestamp(df.loc[index,"Car Time"])
    df.loc[index,"Car Time Adjusted"] = time_in_traffic(coords,departure_time)
    df.to_csv("output/output.csv")
