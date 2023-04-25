import numpy as np
import pandas as pd
import os
from inspect import getsourcefile
from os.path import abspath

import plotly.express as px
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

mapbox_access_token = os.environ['MAPBOX_KEY']
username = 'markedwardson' # your plotly username
api_key = os.environ["PLOTLY_API_KEY"] # your plotly api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

#set active directory to file location
directory = abspath(getsourcefile(lambda:0))
#check if system uses forward or backslashes for writing directories
if(directory.rfind("/") != -1):
    newDirectory = directory[:(directory.rfind("/")+1)]
else:
    newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

stops = pd.read_csv("OpenData_TTC_Schedules/stops.txt")

stop_times = pd.read_csv("OpenData_TTC_Schedules/stop_times.txt")

def fix_hour(hour_str):
    x = hour_str.find(':')
    hour = int(hour_str[:x])
    if hour >= 24:
        hour -= 24
    return(f'{hour:02d}{hour_str[x:]}')

# Apply the fix_hour function to arrival_time
stop_times['arrival_time'] = stop_times['arrival_time'].apply(fix_hour)

stop_times['arrival_time'] = pd.to_datetime(stop_times['arrival_time'])

print("Fixed stop data")

def map(stops,title = "Weekly Victoria bus activity"):
    fig = px.density_mapbox(stops, lat='stop_lat', lon='stop_lon', z='count', radius=15,
                            center=dict(lat=0, lon=180), zoom=0,
                            mapbox_style="stamen-terrain",range_color=[0, 4500],
                            )

    fig.update_layout(
            title = title,
            title_x = 0.5,
            #increase title size
            title_font_size=20,
            #rename colorbar
            coloraxis_colorbar=dict(
                title="Stop count"
            ),
            
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style = "dark",
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=np.average(stops["stop_lat"]),
                    lon=np.average(stops["stop_lon"])
                ),
                pitch=0,
                zoom=10
        
        ))

    #add a paragraph below
    fig.add_annotation(
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        text="Data from BC Transit's static GTFS.Brighter points correspond to stops with more activity (i.e. more routes/trips stop there).",
        showarrow=False,
        font=dict(
            size=13)
        
    )
    return fig

def lookup(stop_id):
    #count how many times stop_id appears in stop_times['stop_id'] and arrival time is after 22:00
    #departure_time column has data like 16:25:00
    
    count = len(stop_times[stop_times["stop_id"] == stop_id])
    return(count)


#main map
stops['count'] = stops['stop_id'].apply(lookup)
fig = map(stops,"TO bus activity")
py.plot(fig,filename="TO Stop activity", auto_open=True)

#late night map
#filter for stops after 1am and before 4:00am
stop_times = stop_times[(stop_times['arrival_time'] > '22:00:00') | (stop_times['arrival_time'] < '04:00:00')]
#plot a histogram of the arrival times

hist = px.histogram(stop_times, x="arrival_time", nbins=24, title="Late night bus activity (10pm - 4am))")
hist.show()

stop_times['arrival_time']
print(stop_times)

stops['count'] = stops['stop_id'].apply(lookup)

fig = map(stops,"Late night TO bus activity")

py.plot(fig,filename="TO Stop activity - after 10", auto_open=True)
