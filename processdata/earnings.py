#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


import fred
import pandas_datareader.data as web
import datetime as dt
import ipywidgets as widgets
from plotly.offline import iplot
from ipywidgets import interact, interact_manual

def get_df():
    my_fred_api_key = 'cd1c1e1224ddd17fc209434088213729'
    fred.key(my_fred_api_key)

    states = {
            '01':'Alabama',
            '02':'Alaska',
            '04':'Arizona',
            '05':'Arkansas',
            '06':'California',
            '08':'Colorado',
            '09':'Connecticut',
            '10':'Delaware',
            '11':'District of Columbia',
            '12':'Florida',
            '13':'Georgia',
            '15':'Hawaii',
            '16':'Idaho',
            '17':'Illinois',
            '18':'Indiana',
            '19':'Iowa',
            '20':'Kansas',
            '21':'Kentucky',
            '22':'Louisiana',
            '23':'Maine',
            '24':'Maryland',
            '25':'Massachusetts',
            '26':'Michigan',
            '27':'Minnesota',
            '28':'Mississippi',
            '29':'Missouri',
            '30':'Montana',
            '31':'Nebraska',
            '32':'Nevada',
            '33':'New Hampshire',
            '34':'New Jersey',
            '35':'New Mexico',
            '36':'New York',
            '37':'North Carolina',
            '38':'North Dakota',
            '39':'Ohio',
            '40':'Oklahoma',
            '41':'Oregon',
            '42':'Pennsylvania',
            '44':'Rhode Island',
            '45':'South Carolina',
            '46':'South Dakota',
            '47':'Tennessee',
            '48':'Texas',
            '49':'Utah',
            '50':'Vermont',
            '51':'Virginia',
            '53':'Washington',
            '54':'West Virginia',
            '55':'Wisconsin',
            '56':'Wyoming'
    }
    states_abb = list(states.keys())

    len(states_abb)
    result = []
    sdt = dt.datetime(2015, 1, 1)
    edt = dt.datetime(2020, 7, 1)
    for state in states_abb:
        abb = "SMU" + state + "000000500000003SA"
        try:
            data = web.DataReader(abb, "fred", sdt, edt)
            result.append(data)       
        except:
            continue
    df = pd.concat([df.iloc[:,0] for df in result],axis=1)
    df.columns = ('AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY')
    return df

def map_widget():
    df = get_df()
    dates = df.index.tolist()
    visual = widgets.Dropdown(
        options=dates,
        description='Year & Month to Choose:')
    
    data = df.loc[date,:].T
    states = data.index
    ur = data.values
    data = [dict(
            type='choropleth',
            autocolorscale = False,
            locations = states,
            z = ur,
            locationmode = 'USA-states',
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                ) ),
            colorbar = dict(
                title = "State Average Hourly Earnings ($)")
            ) ]

    layout = dict(
        title = 'Average Hourly Earnings Distribution - Total Private',
        geo = dict(
            scope = 'usa',
            projection=dict(type='albers usa'),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)')
    )

    fig = dict(data=data, layout=layout)
    fig.show()
    return iplot(fig, filename='d3-cloropleth-map')
    #return interact(show_map, date=visual)


    map_widget()


