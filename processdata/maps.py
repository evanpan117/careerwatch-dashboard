import json
from urllib.request import urlopen
import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Layout
from plotly.offline import plot
import plotly.figure_factory as ff
from . import getdata, earnings

def usa_city_popu():
    df = getdata.city_population()
    fig = px.line(df, y="UNRATE")
    plot_div = plot(fig, include_plotlyjs=True, output_type='div', config={'displayModeBar': True})
    return plot_div

def usa_county_popu():
    df= getdata.usa_counties()
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    fig = px.choropleth(df, geojson=counties, locations='Region Code', color='2020 June',
                                hover_name ='Region Name',
                            color_continuous_scale="YlOrRd",
                            range_color=(0, 20),
                            scope="usa",
                            labels={'unemp':'unemployment rate'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.show()
        
    plot_div = plot(fig, filename='Choropleth Map Creation', include_plotlyjs=True, output_type='div', config={'displayModeBar': True})
        #plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})
        #return plot_div
    return plot_div