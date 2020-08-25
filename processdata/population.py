'''
pip install plotly --upgrade
pip install geopandas==0.3.0
pip install pyshp==1.2.10
pip install shapely==1.6.3
'''

import plotly.figure_factory as ff
import pandas as pd 
from plotly.offline import iplot

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
#df.to_csv(r'/Users/macbookpro15/Dev/careerwatch/Software/Evan/us_population.csv')
df = pd.read_csv('/Users/macbookpro15/Dev/careerwatch/Software/Evan/us_population.csv')

# list values
values = df['TOT_POP'].tolist()
fips = df['FIPS'].tolist()

#have to have the colorscale values at least = to the # of counties
colorscale = ["#399e23", "#47ed21", "#90fc03", "#b8f011", "#f5d742", "#ffcc00", "#ffbb00",
              "#ffa600", "#ff9100", "#ff6f00", "#ff5500", "#ff3c00", "#ff0400", "#ff006a",    
              "#ff00a6", "#ff00cc", "#ad1890", "#822470", "#69275c", "#4f2446", "#241521",
             ]
endpoints = []
for i in range(1,20):
    endpoints.append(10000*i**2.1)
print(endpoints)
fig = ff.create_choropleth(
      fips=fips, values=values, scope=['usa'],
      binning_endpoints = endpoints,colorscale=colorscale, 
      round_legend_values=1,
      simplify_county=0.02, simplify_state=0.02,
      county_outline={'color': 'rgb(15,15,55)', 'width': 0.5},
      state_outline={'width': 0.5},
      legend_title='Population Per County',
      title='California')
    
    
iplot(fig, filename='Choropleth Map Creation')