from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
import json
from . import getdata, maps


def index(request): 
    usa_county_popu_dict = usa_county_popu()
    context = dict(**usa_county_popu_dict)
    return render(request, template_name='index.html', context=context)

def usa_county_popu():
    plot_div = maps.usa_county_popu()
    return {'usa_county_popu': plot_div}

def indexpage(request):
    plot_div = maps.usa_city_popu()
    return render(request, template_name='index.html', context=dict(**{'usa_city_popu': plot_div}))

def mapspage(request):
    plot_div = maps.usa_city_popu()
    return render(request, template_name='pages/maps.html', context={'usa_city_popu': plot_div})


def report(request):
    df = getdata.daily_report(date_string=None)
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f'{(df.Deaths / df.Confirmed)*100:.02f}%'

    data = {
        'num_confirmed': int(df.Confirmed),
        'num_recovered': int(df.Recovered),
        'num_deaths': int(df.Deaths),
        'death_rate': death_rate
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def trends(request):
    df = getdata.percentage_trends()

    data = {
        'confirmed_trend': int(round(df.Confirmed)),
        'deaths_trend': int(round(df.Deaths)),
        'recovered_trend': int(round(df.Recovered)),
        'death_rate_trend': float(df.Death_rate)
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def global_cases(request):
    df = getdata.global_cases()
    return HttpResponse(df.to_json(orient='records'), content_type='application/json')


def realtime_growth(request):
    import pandas as pd
    df = getdata.realtime_growth();

    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')

    return HttpResponse(df.to_json(orient='columns'), content_type='application/json')


def daily_growth(request):
    df_confirmed = getdata.daily_confirmed()[["date", "World"]]
    df_deaths = getdata.daily_deaths()[["date", "World"]]

    df_confirmed = df_confirmed.set_index("date")
    df_deaths = df_deaths.set_index("date")

    json_string = '{' + \
        '"confirmed": ' + df_confirmed.to_json(orient='columns') + ',' + \
        '"deaths": ' + df_deaths.to_json(orient='columns') + \
    '}'

    return HttpResponse(json_string, content_type='application/json')


