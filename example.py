import datetime
import platform

import pandas as pd
import json
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Layout
from plotly.offline import plot
#from getdata.py 
#daily_report() gets data from CSV file on Github and returns dateframe df
def daily_report(date_string=None):
    # Reports aggegrade data, dating as far back to 01-22-2020
    # If passing arg, must use above date formatting '01-22-2020'
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    if date_string is None: 
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else: 
        file_date = date_string 
    
   # df = pd.read_csv(report_directory + file_date + '.csv', dtype={"FIPS": str})

    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
#data column names: City,State,Population,lat,lon


    return df

#from maps
#world_map() gets df from dail_report() and sets up a Plotly Express Fifure fig and returns it
def world_map():
    # Use following Mapbox token to acces further styling features.
    # px.set_mapbox_access_token(open('.mapbox_token').read(''))
    # Reference: https://plotly.com/python/reference/#scattermapbox
    df = daily_report()
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=370)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})
    
    return plot_div

world_map()


def index(request): 
    usa_county_popu_dict = usa_county_popu()
    context = dict(**usa_county_popu_dict)
    return render(request, template_name='index.html', context=context)

def usa_county_popu():
    plot_div = maps.usa_county_popu()
    return {'usa_county_popu': plot_div}