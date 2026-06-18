import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# Read data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = Dash(__name__)

app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site}
                 for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0',
               2500: '2500',
               5000: '5000',
               7500: '7500',
               10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

# Pie Chart Callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df.groupby('Launch Site')['class']
                     .sum()
                     .reset_index(),
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {entered_site}'
        )

    return fig


# Scatter Plot Callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(entered_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Outcome'
        )

    else:

        site_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Outcome for {entered_site}'
        )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
