
'''
1. Prepare the data for the UI - month, day, region, country, state, city, attack type
2. Create the new UI components - dropdwon for all 
3. Link the data with the UI
4. Create callbacks for Auto Filtering 
5. Show the Map
'''


import pandas as pd
import dash   # !pip install dash
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_core_components as dcc

import plotly.graph_objects as go
import plotly.express as px


import webbrowser

# Global Variables
app = dash.Dash()  # Creating your object 


def load_data():
    dataset_name = 'global_terror.csv'
    
    global df
    df = pd.read_csv(dataset_name)
    
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
    month_list= [{"label":key, "value":values} for key,values in month.items()]
    #print(month_list)

    global date_list
    date_list = [{"label":x, "value":x} for x in range(1, 32)] 
    #print(date_list)

    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
    #print(region_list)  
 
    #print(df.sample(5))
    temp_list = sorted(df['country_txt'].unique().tolist())
    #print(temp_list)
    global country_list
    # List comprehension
    country_list = [{"label": str(i), "value": str(i)}  for i in temp_list ]
    #print(country_list)


    global state_list
    state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
    #print(state_list)
    # Total 2580 states

    global city_list
    city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
    #print(city_list)
    # Total 39489 cities

    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
    #print(attack_type_list)


    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    #print(year_list)

    global year_dict
    # my slider needs data in dictionary format 
    year_dict = {str(year): str(year) for year in year_list}
    #print(year_dict)


def open_browser():
    # Opening the Browser
    webbrowser.open_new('http://127.0.0.1:8050/')

def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div(
    [
    html.H1('Terrorism Analysis with Insights', id='Main_title'),
    
    dcc.Dropdown(
          id='month', 
          options=month_list,
          placeholder='Select Month',
    ),
    dcc.Dropdown(
          id='date', 
          options=date_list,
          placeholder='Select Day',
    ),
    dcc.Dropdown(
          id='region-dropdown', 
          options=region_list,
          placeholder='Select Region',
    ),
    dcc.Dropdown(
          id='country-dropdown', 
          options=country_list,#[{'label': 'All', 'value': 'All'}],
          placeholder='Select Country'
    ),
    dcc.Dropdown(
          id='state-dropdown', 
          options=state_list,#[{'label': 'All', 'value': 'All'}],
          placeholder='Select State or Province'
    ),
    dcc.Dropdown(
          id='city-dropdown', 
          options=city_list,#[{'label': 'All', 'value': 'All'}],
          placeholder='Select City'
    ),
    dcc.Dropdown(
          id='attacktype-dropdown', 
          options=attack_type_list,
          placeholder='Select Attack Type'
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
    dcc.Graph(id='graph-object')
    ]
    )
    
    return main_layout

# Callback of your page
@app.callback(
    dash.dependencies.Output('graph-object', 'figure'),
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
  
  df1 = df
  #df1 = # write some logic to change data 

  # You should always set the figure for blank, since this callback 
  # is called once when it is drawing for first time
  figure = go.Figure()


  figure = px.scatter_mapbox(df1,
                        lat="latitude", 
                        lon="longitude",
                        hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear"],
                        zoom=1
            )                       

  figure.update_layout(mapbox_style="open-street-map",
                    autosize=True,
                    margin=dict(l=0, r=0, t=25, b=20),
  )

  return figure




@app.callback(
  Output("date", "options"),
  [
  Input("month", "value")
  ]
  )
def update_date(month):
    date_list = [x for x in range(1, 32)]

    if month in [1,3,5,7,8,10,12]:
        # returing 1 to 31
        return [{"label":m, "value":m} for m in date_list]
    elif month in [4,6,9,11]:
        # returning 1 to 30
        return [{"label":m, "value":m} for m in date_list[:-1]]
    elif month==2:
        # returning 1 to 29
        return [{"label":m, "value":m} for m in date_list[:-2]]
    else:
        return []


@app.callback(
    Output('country-dropdown', 'options'),
    [
    Input('region-dropdown', 'value')
    ]
    )
def set_country_options(region_value):
  # Making the country dropdwown data

  return[{"label": str(i), "value": str(i)}  for i in df[df['region_txt'] == region_value] ['country_txt'].unique().tolist() ]




@app.callback(
    Output('state-dropdown', 'options'),
    [
    Input('country-dropdown', 'value')
    ]
    )
def set_state_options(country_value):
  # Making the state Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'] == country_value] ['provstate'].unique().tolist() ]




@app.callback(
    Output('city-dropdown', 'options'),
    [
    Input('state-dropdown', 'value')
    ]
    )
def set_city_options(state_value):
  # Making the city Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'] == state_value] ['city'].unique().tolist() ]



    
def main():
    print("Welcome to the Project Season 3 ")   
    
    load_data()
    open_browser()
    
    global app
    
    app.layout = create_app_ui()  # blank Container Page
    # change the title
    app.title = "Terrorism Analysis with Insights"

    # Change the favicon 
    # https://www.favicon.cc/  upload your icon for your project  download your favicon
    # create a directory assests  and copy your favicon.ico there


    app.run_server()
    
    print("Thanks for using my Project ")
    # Industry Best Practices 
    app = None 
    df = None 

# pl do  not type your code here 

if __name__ == '__main__' :
    main()


'''
style={'background-image': 'url(assets/military.jpeg)'}
'''






