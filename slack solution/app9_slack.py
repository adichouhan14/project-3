# Multi selection in the dropdowns

#importing the libraries
import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate


# Global variables
app = dash.Dash()


def load_data():
  dataset_name = 'dataset\global_terror.csv'

  #this line we use to hide some warnings which gives by pandas
  #pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  
  #pd.set_option("display.max_rows", None)
  #pd.set_option('display.max_columns', None)
  #print(df.head(5))
  #print(df.tail(5))

  global month_list
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
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [{"label":x, "value":x} for x in range(1, 32)] 


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  #region_list.insert(0, {"label":"All", "value":"All"} )

  #print(region_list)  
  # Total 12 Regions

  global country_list
  #country_list = [{"label": str(i), "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())]
  #print(country_list)
  # Total 205 Countries
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  global state_list
  #state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
  #print(state_list)
  # Total 2580 states
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()


  global city_list
  #city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
  #print(city_list)
  # Total 39489 cities
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  #print(attack_type_list)


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  #print(year_dict)



def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div(
  [
  html.H1('Terrorism Analysis with Insights', id='Main_title'),
  html.Div(html.Div(id='my_hidden')),
  dcc.Dropdown(
        id='month', 
        options=month_list,
        placeholder='Select Month',
        multi = True
  ),
  dcc.Dropdown(
        id='date', 
        placeholder='Select Day',
        multi = True
  ),
  dcc.Dropdown(
        id='region-dropdown', 
        options=region_list,
        placeholder='Select Region',
        multi = True
  ),
  dcc.Dropdown(
        id='country-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select Country',
        multi = True
  ),
  dcc.Dropdown(
        id='state-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select State or Province',
        multi = True
  ),
  dcc.Dropdown(
        id='city-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select City',
        multi = True
  ),
  dcc.Dropdown(
        id='attacktype-dropdown', 
        options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
        placeholder='Select Attack Type',
        multi = True
  ),

  html.H5('Select the Year', id='year_title'),
  dcc.RangeSlider(
        id='year-slider',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict
  ),
  html.Br(),
  html.Div(id='graph-object', children = ["World Map is loading"])
  ]
  )
  
  return main_layout


# Callback of your page
@app.callback(
    dash.dependencies.Output('graph-object', 'children'),
    [
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value')
    ]
    )

def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
  
    print("Data Type of month value = " , str(type(month_value)))
    print("Data of month value = " , month_value)
    
    print("Data Type of Day value = " , str(type(date_value)))
    print("Data of Day value = " , date_value)
    
    print("Data Type of region value = " , str(type(region_value)))
    print("Data of region value = " , region_value)
    
    print("Data Type of country value = " , str(type(country_value)))
    print("Data of country value = " , country_value)
    
    print("Data Type of state value = " , str(type(state_value)))
    print("Data of state value = " , state_value)
    
    print("Data Type of city value = " , str(type(city_value)))
    print("Data of city value = " , city_value)
    
    print("Data Type of Attack value = " , str(type(attack_value)))
    print("Data of Attack value = " , attack_value)
    
    print("Data Type of year value = " , str(type(year_value)))
    print("Data of year value = " , year_value)
  
  

    # year_filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df = df[df["iyear"].isin(year_range)]
    
    # month_filter
    if month_value==[] or month_value is None:
        pass
    else:
        if date_value==[] or date_value is None:
            new_df = new_df[new_df["imonth"].isin(month_value)]
        else:
            new_df = new_df[new_df["imonth"].isin(month_value)
                            & (new_df["iday"].isin(date_value))]
              
              
    # region, country, state, city filter
    if region_value==[] or region_value is None:
        pass
    else:
        if country_value==[] or country_value is None :
            new_df = new_df[new_df["region_txt"].isin(region_value)]
        else:
            if state_value == [] or state_value is None:
                new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value))]
            else:
                if city_value == [] or city_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value)) &
                                (new_df["provstate"].isin(state_value))]
                else:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value)) &
                                    (new_df["provstate"].isin(state_value))&
                                    (new_df["city"].isin(city_value))]
    
    if attack_value == [] or attack_value is None:
        pass
    else:
        new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]
                        
    
    
    # You should always set the figure for blank, since this callback 
    # is called once when it is drawing for first time        
    # figure = go.Figure()
    
    if new_df.shape[0]:
        pass
    else: 
        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        
        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]

    
    figure = px.scatter_mapbox(new_df,
                  lat="latitude", 
                  lon="longitude",
                  color="attacktype1_txt",
                  hover_name="city", 
                  hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                  zoom=1
                  )                       
    figure.update_layout(mapbox_style="open-street-map",
              autosize=True,
              margin=dict(l=0, r=0, t=25, b=20),
              )
  
    return dcc.Graph(figure=figure)
    

@app.callback(
  Output("date", "options"),
                [Input("month", "value")])
def update_date(month):
    date_list = [x for x in range(1, 32)]
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option


@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app_ui()
  app.title = "Terrorism Analysis with Insights"
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() # debug=True

  print("This would be executed only after the script is closed")
  df = None
  app = None



if __name__ == '__main__':
    main()


