# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\kggha\Documents\Coursera\IBM Data Science Course\Applied Data Science Capstone\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label':'All Sites', 'value':'All Sites'},
                                                      {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                      {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                                      {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                      {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                            )
                                        ,
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(value):
    filter_df = spacex_df
    if value == 'All Sites':
        fig1 = px.pie(filter_df, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig1
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==value]
        a = filtered_df[filtered_df['class'] == 0].count()
        b = filtered_df[filtered_df['class'] == 1].count()
        fig_data = pd.DataFrame({'0':a, '1':b}).transpose()
        title = 'Total Success Launches for site ' + value
        fig1 = px.pie(fig_data, values='class', names=['0','1'], title=title)
        return fig1
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(value1, value2):
    filtered_df2 = spacex_df[(spacex_df['Payload Mass (kg)']> value2[0]) & (spacex_df['Payload Mass (kg)']<value2[1])]
    if value1 == 'All Sites':
        fig2 = px.scatter(filtered_df2, x = 'Payload Mass (kg)', y='class',
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for all Sites')
        return fig2
    else:
        filter_df = filtered_df2[filtered_df2['Launch Site']==value1]
        title = 'Correlation Between Payload and Success for ' + value1
        fig2 = px.scatter(filter_df, x = 'Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=title)
        return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
