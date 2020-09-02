
import datetime as dt
import platform
import pandas as pd
import fred
import pandas_datareader.data as web

my_fred_api_key = 'f18267cd179d1658737f4a68e3e8c664'
fred.key(my_fred_api_key)

# Different styles in zero-padding in date depend on operating systems
if platform.system() == 'Linux':
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
elif platform.system() == 'Windows':
    STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'
else:
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'

def usa_counties():
    df= pd.read_excel("GeoFRED_Unemployment_Rate_by_County_Percent.xls", skiprows=1, dtype={"Region Code": str})
    return df

def city_population():
    sdt = dt.datetime(1976, 1, 1)
    edt = dt.datetime(2020, 7, 1)
    df = web.DataReader("UNRATE", "fred", sdt, edt)
    return df
    
def plotly_time_series():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    return df

def daily_confirmed():
    # returns the daily reported cases for respective date, 
    # segmented globally and by country
    df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_cases.csv')
    return df


def daily_deaths():
    # returns the daily reported deaths for respective date
    df = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/new_deaths.csv')
    return df


def confirmed_report():
    # Returns time series version of total cases confirmed globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    return df


def deaths_report():
    # Returns time series version of total deaths globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    return df


def recovered_report():
    # Return time series version of total recoveries globally
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return df 


def realtime_growth(date_string=None, weekly=False, monthly=False):
    """[summary]: consolidates all reports, to create time series of statistics.
    Columns excluded with list comp. are: ['Province/State','Country/Region','Lat','Long'].

    Args:
        date_string: must use following date formatting '4/12/20'.
        weekly: bool, returns df for last 8 weks
        monthly: bool, returns df for last 3 months
    Returns:
        [growth_df] -- [growth in series]
    """ 
    df1 = confirmed_report()[confirmed_report().columns[4:]].sum()
    df2 = deaths_report()[deaths_report().columns[4:]].sum()
    df3 = recovered_report()[recovered_report().columns[4:]].sum()
    
    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'] = df1, df2, df3
    growth_df.index = growth_df.index.rename('Date')
    
    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)
    
    if date_string is not None: 
        return growth_df.loc[growth_df.index == date_string]
    
    if weekly is True: 
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index==day])
        return weekly_df
    
    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index==day])
        return monthly_df
    
    return growth_df


def percentage_trends():
    """[summary]: Returns percentage of change, in comparison to week prior.
    
    Returns:
        [pd.series] -- [percentage objects]
    """    
    current = realtime_growth(weekly=True).iloc[-1]
    last_week = realtime_growth(weekly=True).iloc[-2]
    trends = round(number=((current - last_week)/last_week)*100, ndigits=1)
    
    rate_change = round(((current.Deaths/current.Confirmed)*100)-((last_week.Deaths / last_week.Confirmed)*100), ndigits=2)
    trends = trends.append(pd.Series(data=rate_change, index=['Death_rate']))
    
    return trends


def global_cases():
   
    df = daily_report()[['Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    df.rename(columns={'Country_Region':'Country'}, inplace=True) 
    df = df.groupby('Country', as_index=False).sum()  # Dataframe mapper, combines rows where country value is the same
    df.sort_values(by=['Confirmed'], ascending=False, inplace=True)
    
    return df

