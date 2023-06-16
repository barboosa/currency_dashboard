from dash import dcc, html
from dash import Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import requests
import datetime
from datetime import datetime as dt
import scipy.spatial as sp
import scipy.cluster.hierarchy as hc
import numpy as np
from dash.exceptions import PreventUpdate


def generate_ordering(df):
    dist_matrix = np.sqrt(0.5*(1-df))
    linkage = hc.linkage(sp.distance.squareform(dist_matrix), method='ward')
    leaves = hc.leaves_list(linkage)
    col_order = [df.columns[i] for i in leaves]
    return col_order

def generate_correlation_matrix(start_date_str, end_date_str, fixed_order=None):
    data = requests.get(
        f'http://127.0.0.1:8000/currencies/currency-correlations?start_date={start_date_str}&end_date={end_date_str}').json()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.replace('=X', '')
    df.index = df.index.str.replace('=X', '')
    if fixed_order is not None:
        df = df.loc[fixed_order, fixed_order]
    return df



def generate_figure(df):
    figure = go.Figure(
        data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.columns,
            colorscale='RdBu',
            colorbar=dict(title='Correlation Coefficient'),
            hoverongaps=False
        ),
        layout=go.Layout(
            title="Currency Correlation Matrix",
            xaxis=dict(ticks='', nticks=len(df.columns)),
            yaxis=dict(ticks='', nticks=len(df.columns)),
            autosize=True,
        )
    )
    return figure


end_date = datetime.datetime.now() - datetime.timedelta(days=1)
start_date = datetime.datetime.now() - datetime.timedelta(days=120)

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

fixed_start_date = datetime.datetime(2019, 6, 1)
fixed_end_date = datetime.datetime(2023, 6, 1)
fixed_start_date_str = fixed_start_date.strftime('%Y-%m-%d')
fixed_end_date_str = fixed_end_date.strftime('%Y-%m-%d')

fixed_df = generate_correlation_matrix(
    fixed_start_date_str, fixed_end_date_str)
fixed_order = fixed_df.columns.tolist()

df = generate_correlation_matrix(start_date_str, end_date_str, fixed_order)
figure = generate_figure(df)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(className='flex-container-align-left', children=[
                html.H5("Select Date Range:", className="label-margin"),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=datetime.datetime(1980, 1, 1),
                    max_date_allowed=datetime.datetime.now() - datetime.timedelta(days=1),
                    start_date=start_date,
                    end_date=end_date,
                    className='dcc_control'
                ),
            ])
        ]),
        dbc.Col([
            html.Div(className='flex-container-align-left', children=[
                html.H5("Select Reordering Date Range:", className="label-margin"),
                dcc.DatePickerRange(
                    id='reorder-date-picker',
                    min_date_allowed=datetime.datetime(1980, 1, 1),
                    max_date_allowed=datetime.datetime.now() - datetime.timedelta(days=1),
                    start_date=start_date,
                    end_date=end_date,
                    className='dcc_control'
                ),
            ])
        ])
    ]),
    dcc.Loading(
        id="loading",
        type="circle",
        children=[dcc.Graph(
            id='heatmap',
            style={'height': '80vh'},
            figure=figure
        )]
    )
])


@callback(
    Output('heatmap', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('reorder-date-picker', 'start_date'),
     Input('reorder-date-picker', 'end_date')]
)
def update_graph(start_date, end_date, reorder_start_date, reorder_end_date):
    start_date = dt.strptime(start_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = dt.strptime(end_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
    reorder_start_date = dt.strptime(reorder_start_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
    reorder_end_date = dt.strptime(reorder_end_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')

    df = generate_correlation_matrix(reorder_start_date, reorder_end_date)
    fixed_order = generate_ordering(df)

    df = generate_correlation_matrix(start_date, end_date, fixed_order)
    figure = generate_figure(df)
    return figure
