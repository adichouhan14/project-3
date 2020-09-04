# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 19:50:05 2020

@author: adichouhanofficial
"""
# importing the libraries
import webbrowser
import pandas as pd

import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_core_components as dcc

import plotly.graph_objects as go
import plotly.express as px

from dash.exceptions import PreventUpdate

#global variable
app=dash.Dash()

def load_data():
    dataset_name='dataset\global_terror.csv'
    
    global df
    df=pd.read_csv(dataset_name)
   # print(df.head())
    
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }

    global month_list
    month_list=[{'label':key,'value':value} for key,value in month.items()]
    
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in sorted(df['region_txt'].unique().tolist()) ]
    #print(region_list)

    global year_list
    year_list=sorted(df['iyear'].unique().tolist())
    #print(country_names)
    #print(year_list)
    
    global year_dict
    year_dict={ str(i):str(i) for i in year_list }
    #print(country_dict)
    #print(year_dict)

    global attack_list
    attack_list=[{'label':str(i),'value':str(i)} for i in sorted(df['attacktype1_txt'].unique().tolist())]

def open_browser():
    #Opening browser
    webbrowser.open_new('http://127.0.0.1:8050/')
  
#Layout of your page
def create_app_ui():
    #Designing web page
    main_layout=html.Div([
    html.H1(id='main_title', children='Terrorism Analysis with Insights'),
    dcc.Tabs(id='Tabs',value='tab-1',children=[
        dcc.Tab(label='Map tool', id='Map-tool',value='tab-1',children=[
            dcc.Tabs(id='subtabs',value='tab-1',children=[
                dcc.Tab(label='World Map tool',id='World',value='tab-1',children=[
                   
                    html.Div(html.Div(id='my-hidden')),
                    dcc.Dropdown(id='month', options=month_list, placeholder='Select Month',multi=True),
                    dcc.Dropdown(id='date',  placeholder='Select Date',multi=True),
                    dcc.Dropdown(id='region-dropdown', options=region_list, placeholder='Select Region',multi=True),
                    dcc.Dropdown(id='country-dropdown',  placeholder='Select Country',multi=True),
                    dcc.Dropdown(id='state-dropdown',  placeholder='Select State',multi=True),
                    dcc.Dropdown(id='city-dropdown',  placeholder='Select City',multi=True),
                    dcc.Dropdown(id='attack-dropdown', options=attack_list, placeholder='Select Attack',multi=True),
                                
                    html.H5('Select the Year', id='year_title'),
                            
                    dcc.RangeSlider(
                        id='year-slider',
                        min=min(year_list),
                        max=max(year_list),
                        value=[min(year_list),max(year_list)], #default value of slider
                        marks=year_dict   # this is the interval for slider
                        ),
                    html.Br(),
                    html.Div(id='graph-object',children=["World Map is loading"])
                    ]),
                dcc.Tab(label='India Map tool',id='India',value='tab-2',children=[html.Div()])
                    ])]),

            dcc.Tab(label='Chart Tool', id='chart-tool',value='Chart',children=[
                dcc.Tabs(id='sub-tabs2',value='tab-2',children=[
                    dcc.Tab(label='World Chart tool',id='World-chart',value='tab-1'),
                    dcc.Tab(label='India Chart tool',id='India-chart',value='tab-2')]),
                    html.Div()
                    ])
            ])
    ])
    return main_layout

#Callback of your page

@app.callback(
    Output('graph-object','figure'),
    [
        Input('month','value'),
        Input('date','value'),
        Input('region-dropdown','value'),
        Input('country-dropdown','value'),
        Input('state-dropdown','value'),
        Input('city-dropdown','value'),
        Input('attack-dropdown','value'),
        Input('year-slider','value'),
    ])

def update_map(month,date,region,country,state,city,attack,year):

    print("Data Type of month value = " , str(type(month)))
    print("Data of month value = " , month)

    print("Data Type of Day value = " , str(type(date)))
    print("Data of Day value = " , date)

    print("Data Type of region value = " , str(type(region)))
    print("Data of region value = " , region)

    print("Data Type of country value = " , str(type(country)))
    print("Data of country value = " , country)

    print("Data Type of state value = " , str(type(state)))
    print("Data of state value = " , state)

    print("Data Type of city value = " , str(type(city)))
    print("Data of city value = " , city)

    print("Data Type of Attack value = " , str(type(attack)))
    print("Data of Attack value = " , attack)

    print("Data Type of year value = " , str(type(year)))
    print("Data of year value = " , year)
    
   # year filter
    year_range = range(year[0],year[1]+1)
    new_df=df[df['iyear'].isin(year_range)]

   #month filter
    if month==[] or month is None:
        pass
    else:
        if date==[] or date is None:
            new_df=new_df[new_df['imonth'].isin(month)]
        else:
            new_df=new_df[new_df['imonth'].isin(month) & (new_df['iday'].isin(date))]

    if Tab=='tab-1':
        if subtabs=='tab-2':
            raise PreventUpdate
        else:

            #region , country, state, city filter
            if region ==[] or region is None:
                pass
            else:
                if country==[] or country is None:
                    new_df=new_df[ (new_df['region_txt'].isin(region)) & (new_df['country_txt'].isin(country))]

                else:
                    if city==[] or city is None:
                        new_df=new_df[ (new_df['region_txt'].isin(region)) & (new_df['country_txt'].isin(country)) & (new_df['provstate'].isin(state))]
                    else:
                        new_df=new_df[ (new_df['region_txt'].isin(region)) & (new_df['country_txt'].isin(country)) & (new_df['provstate'].isin(state)) &  (new_df['city'].isin(city))]

            if attack==[] or attack is None:
                pass
            else:
                new_df=new_df[new_df['attacktype1_txt'].isin(attack)]

            #You should always set the figure for blank since this callback
            #is called once when it is drawing for the first time
            figure=go.Figure()
            if new_df.shape[0]:
                pass
            else:
                new_df=pd.DataFrame(columns=[
                    'iyear','imonth','iday','country_txt','region_txt','provstate','city','latitude','longitude','attacktype1_txt','nkill'])

                new_df.loc[0]=[0,0,0,None,None,None,None,None,None,None,None]

            figure=px.scatter_mapbox(df1,
                                     lat='latitude',
                                     lon='longitude',
                                     color='attacktype1_txt',
                                     hover_name='city',
                                     hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear"],
                                     zoom=1.5)

            figure.update_layout(mapbox_style='open-street-map',autosize=True,margin=dict(l=25, r=25, t=0, b=20))
    
            return dcc.Graph(figure=figure)
    else:
        raise PreventUpdate
    


@app.callback(
    Output('date','options'),
    [Input('month','value')]
)
def update_date(month):
    if month in [1,3,5,7,8,10,12]:
        return [{'label':dd,'value':dd} for dd in range(1,32)]
    if month in [4,6,9,11]:
        return [{'label':dd,'value':dd} for dd in range(1,31)]
    if month==2:
        return [{'label':dd,'value':dd} for dd in range(1,30)]
    return []

@app.callback(
    Output('country-dropdown','options'),
    [Input('region-dropdown','value')]
)
def update_country(region):
    return [{'label':str(i),'value':str(i)} for i in sorted(df[df['region_txt']==region]['country_txt'].unique().tolist())]

@app.callback(
    Output('state-dropdown','options'),
    [Input('country-dropdown','value')]
)
def update_state(country):
    return [{'label':str(i),'value':str(i)} for i in sorted(df[df['country_txt']==country]['provstate'].unique().tolist())]

@app.callback(
    Output('city-dropdown','options'),
    [Input('state-dropdown','value')]
)
def update_city(state):
    return [{'label':str(i),'value':str(i)} for i in sorted(df[df['provstate']==state]['city'].unique().tolist())]


def main():
    print("Welcome to the project season3")
    
    load_data()
    open_browser()
    global app
    app.layout=create_app_ui()
    app.title="Terrorism Analysis with Insights"
    #go to https://www.favicon.cc/ and download the ico file and store in assets directory
    app.run_server() #debug=True
    
    print("Thankyou for using my project")
    
    #Industry Best Practice
    app=None
    df=None
    
    
if __name__=="__main__":
    main()
