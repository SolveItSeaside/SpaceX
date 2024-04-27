# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


#I have a csv here spacex_df = pd.read_csv("spacex_launch_dash.csv")
#I want to  Add a dropdown list to enable Launch Site selection for variable Launch Site
#The default select value is for ALL sites
#in the format dcc.Dropdown(id='site-dropdown',...)

# Create a dash application
app = dash.Dash(__name__)
# Create an app layout
# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...)
    html.Label('Select a Launch Site:'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
        ],
        value='ALL'  # Default select value
    ),
    html.Br(),
    html.Div(id='output-container'),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Add a slider to select payload range
    html.Label('Select Payload Range (Kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=100,
        marks={0: '0', 10000: '10000'},
        value=[0, 10000]
    ),
    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Define callback to update output based on dropdown selection
@app.callback(
    Output('output-container', 'children'),
    [Input('site-dropdown', 'value')]
)
def update_output(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df  # Show all sites
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]  # Filter by selected site
    
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in filtered_df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns
            ]) for i in range(min(len(filtered_df), 10))  # Display up to 10 rows
        ])
    ])
@app.callback(
    [Output('success-pie-chart', 'figure'),
     Output('success-payload-scatter-chart', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_charts(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df  # Show all sites
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]  # Filter by selected site
    
    filtered_df_scatter = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                      (filtered_df['Payload Mass (kg)'] <= payload_range[1])]  # Filter by payload range
    
    if selected_site == 'ALL':
        success_counts = spacex_df['class'].value_counts()  # Assuming 'class' is the column representing success/failure
    else:
        filtered_df_pie = filtered_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df_pie['class'].value_counts()  # Assuming 'class' is the column representing success/failure
    
    pie_chart = px.pie(
        names=success_counts.index,
        values=success_counts.values,
        title='Success vs. Failure Counts'
    )
    
    scatter_chart = px.scatter(
        filtered_df_scatter,
        x='Payload Mass (kg)',
        y='class',  # Assuming 'class' is the column representing success/failure
        color='class',  # Assuming 'class' is the column representing success/failure
        title='Correlation between Payload and Launch Success',
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'}
    )
    
    return pie_chart, scatter_chart



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                             #   html.Div(dcc.Graph(id='success-pie-chart')),
                             #   html.Br(),

                              #  html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                              #  html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                              #  ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
