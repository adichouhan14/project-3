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

#global variable
app=dash.Dash()

def load_data():
    dataset_name='dataset\global_terror.csv'
    global df
    df=pd.read_csv(dataset_name)
    print(df.head())
    country_list=sorted(df['country_txt'].unique().tolist())
    global year_list
    year_list=sorted(df['iyear'].unique().tolist())
    #print(country_names)
    #print(year_list)
    global country_dict
    country_dict=[{'label':str(i),'value':str(i)} for i in country_list]
    global year_dict
    year_dict={ str(i):str(i) for i in year_list }
    #print(country_dict)
    #print(year_dict)

def open_browser():
    #Opening browser
    webbrowser.open_new('http://127.0.0.1:8050/')
  
#Layout of your page
def create_app_ui():
    #Designing web page
    main_layout=html.Div([
            html.H1(id='main_title', children='Terrorism Analysis with Insights'),
            #html.Button(id='button_close', children='Click to Test', n_clicks=0),
            #html.Hr(),
            dcc.Dropdown(id='country-dropdown', options=country_dict, value='India'),
			dcc.Graph(id='graph-object'),
            dcc.Slider(
                id='year-slider',
                min=min(year_list),
                max=max(year_list),
                value=min(year_list), #default value of slider
                marks=year_dict   # this is the interval for slider
                )
            ])
    return main_layout
	
'''
@app.callback(
        dash.dependencies.Output('button_close','children'),
        [dash.dependencies.Input('button_close','n_clicks')]
        )

def update_app_ui(n_clicks):
    #Industry best practice
    print('Value passed is =',str(n_clicks))
    
    if n_clicks>0:
        return 'I clicked ='+str(n_clicks)
    else:
        return 'Click to Test'
'''

#Callback of your page
@app.callback(
        dash.dependencies.Output('graph-object','figure'),
        [
		 dash.dependencies.Input('country-dropdown','value'),
         dash.dependencies.Input('year-slider','value')]
        )
def update_app_ui(country_value,year_value):
    #Industry best practice
    print('Data type of country value =',str(type(country_value)))
    print('Data of country value =',str(country_value))
    
    print('Data type of year value =',str(type(year_value)))
    print('Data of year value =',str(year_value))

    figure=go.Figure()
    return figure
    '''
    print('Data type of value =',str(type(dd_value)))
    print('Data of value =',str(dd_value))
    
    #You should always set the figure for black, since this callback
    #is called once when it is drawing for the first time
    figure=go.Figure()
    data=[['mohan',10],['ramesh',15],['ritik',20],['rohan',13],['sita',19]]
    if dd_value=='Bar':
        print("Bar is selected from the drop down")

        figure=px.bar(pd.DataFrame(data,columns=['Name','Age']),
                      y='Age',
                      x='Name',
                      text='Age',
                      hover_data=['Name'],
                      height=500)
    
    elif dd_value=='Line':
        print('Line is selected from the drop down')
        
        figure=go.Figure(data=go.Line(x=pd.DataFrame(data,columns=['Name','Age'])['Name'],y=pd.DataFrame(data,columns=['Name','Age'])['Age']))
     
    else:
        print('Nothing is selected from the drop down')
    return figure
    '''

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