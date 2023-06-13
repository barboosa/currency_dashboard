import requests
import datetime
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime as dt
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

currency_data = requests.get('http://127.0.0.1:8000/currencies').json()
currency_options = [{'label': currency.replace(
    '=X', ''), 'value': currency} for currency in currency_data]

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(className='flex-container-align-left', children=[
                html.H5("Select Date Range:", className="label-margin"),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=datetime.datetime(2000, 1, 1),
                    max_date_allowed=datetime.datetime.today(),
                    start_date=datetime.datetime.now() - datetime.timedelta(days=7),
                    end_date=datetime.datetime.now() - datetime.timedelta(days=1),
                    className='dcc_control'
                )
            ]),
            html.Div(className='flex-container', children=[
                html.H5("Select Currencies:", className="label-margin"),
                dcc.Dropdown(
                    id='currency-selector',
                    options=currency_options,
                    value=[currency['value'] for currency in currency_options],
                    multi=True,
                    className='dcc_control'
                ),
            ]),
            dcc.Loading(
                id="loading",
                type="circle",
                children=[dcc.Graph(
                    id='currency-trends-graph',
                    style={'height': '80vh'},
                )]
            )
        ])
    ])
])


@callback(
    Output('currency-trends-graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('currency-selector', 'value')]
)
def update_graph(start_date, end_date, selected_currencies):
    start_date = dt.strptime(start_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = dt.strptime(end_date.split(
        'T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')

    data = requests.get(
        f'http://127.0.0.1:8000/currencies/historic-prices?start_date={start_date}&end_date={end_date}').json()
    currency_data = {}
    for currency_pair, price_data in data.items():
        currency_label = currency_pair.replace('=X', '')
        if currency_pair in selected_currencies:
            df = pd.DataFrame.from_dict(
                price_data, orient='index', columns=[currency_label])
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df = df.divide(df.iloc[0]).multiply(100)
            currency_data[currency_label] = df

    fig = go.Figure()
    for currency_label, price_data in currency_data.items():
        fig.add_trace(go.Scatter(x=price_data.index, y=price_data[currency_label],
                                 name=currency_label))

    fig.update_layout(title="Currency Trends",
                      xaxis_title="Date",
                      yaxis_title="Indexed Price")

    return fig
