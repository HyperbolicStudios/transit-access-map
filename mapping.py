import pandas as pd
import plotly
import plotly.express as px
import geopandas as gpd

import os
from inspect import getsourcefile
from os.path import abspath
import json

#set active directory to file location
directory = abspath(getsourcefile(lambda:0))
#check if system uses forward or backslashes for writing directories
if(directory.rfind("/") != -1):
    newDirectory = directory[:(directory.rfind("/")+1)]
else:
    newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

def make_maps():
    print("Starting")
    for data_set in ["UBC Data Final.csv"]:
        df = pd.read_csv("data/"+data_set)

        df = df.replace(["???","#VALUE!"],-1)
        df["Transit Time"] = df["Transit Time"].astype(float)
        df["Bike Time"] = df["Bike Time"].astype(float)
        df["Car Time"] = df["Car Time"].astype(float)
        df = df.round(0)

        shape = gpd.read_file("vancouver.geojson")
        shape = shape.to_crs('EPSG:4326')

        shape.id = shape.id.astype(int)
        df.id = df.id.astype(int)

        data = shape
        data["Transit Time"] = df["Transit Time"]
        data["Car Time"] = df["Car Time"]
        data["Bike Time"] = df["Bike Time"]
        print("loaded data")

        print(data.columns)
        for mode in ["Transit Time","Bike Time", "Car Time"]:

            fig = px.choropleth_mapbox(data, geojson=data.geometry, locations=data.index, color=mode,
                                       color_continuous_scale="Viridis",
                                       range_color=(0, 150),
                                       #hover_data = ["id","Transit Time", "Bike Time", "Car Time"],
                                       mapbox_style="carto-positron",
                                       zoom=10, center = {"lat": 49.238048, "lon": -123.096121},
                                       opacity=.5,
                                       custom_data = ['id',"Transit Time","Bike Time","Car Time"]
                                       )
            fig.update_traces(hovertemplate = """
                <b>Census ID:</b> %{customdata[0]} <br>
                <b>transit Time:</b> %{customdata[1]} minutes <br>
                <b>Bike Time:</b> %{customdata[2]} minutes   <br>
                <b>Car Time:</b> %{customdata[3]} minutes"""
                                                 )

            fig.write_html("maps/{}_{}.html".format(data_set[:data_set.find(" ")],mode))
            print('Made figure for {} to {}'.format(mode,data_set))

    print('Done')
    return
make_maps()
