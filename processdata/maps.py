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
    fig = px.scatter_mapbox(
        df, 
        lat="lat", lon="lon", 
        hover_name="City", 
        hover_data=["State", "Population"],
        color_discrete_sequence=["fuchsia"], 
        
        zoom=3, 
        height=450,
        center = {'lat': 38.0, 'lon': -97.0}
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.show()
    plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})
    return plot_div


def usa_county_popu():
    
    df= getdata.usa_counties()

    # list values
    values = df['2020 June'].tolist()
    fips = df['Region Code'].tolist()

    #have to have the colorscale values at least = to the # of counties
    colorscale = [  "#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                     "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                     "#08519c","#0b4083","#08306b", "#072859","#04194f","#040f4f","#08044f",
                ]
    endpoints = []
    for i in range(1,20):
        endpoints.append(i)
    fig = ff.create_choropleth(
        fips=fips, values=values, scope=['usa'],
        binning_endpoints = endpoints,colorscale=colorscale, 
        round_legend_values=1,
        simplify_county=0.02, simplify_state=0.02,
        show_hover=True, show_state_data=True,
        county_outline={'color': 'rgb(15,15,55)', 'width': 0.5},
        state_outline={'width': 0.5},
        legend_title='Unemployment Rate',
        title='USA Unemployment Rate'
        )
        
    plot_div = plot(fig, filename='Choropleth Map Creation', include_plotlyjs=True, output_type='div', config={'displayModeBar': False})
        #plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})
        #return plot_div
    return plot_div