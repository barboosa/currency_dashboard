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
    html.Div([
        html.H2("Select Date Range", className="text-center mt-3 mb-4"),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime.datetime(2020, 1, 1),
            max_date_allowed=datetime.datetime.today(),
            start_date=datetime.datetime.now() - datetime.timedelta(days=7),
            end_date=datetime.datetime.now() - datetime.timedelta(days=1)
        ),
        dcc.Dropdown(
            id='currency-selector',
            options=currency_options,
            value=[currency['value'] for currency in currency_options],
            multi=True,
            className="mt-3"
        ),
        dcc.Loading(
            id="loading",
            type="circle",
            children=[dcc.Graph(
                id='currency-trends-graph',
                style={'height': '80vh'},
            )]
        )
    ], className="mt-5")
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
        currency_label = currency_pair.replace(
            '=X', '')
        if currency_pair in selected_currencies:
            currency_data[currency_label] = pd.DataFrame(price_data, index=[0])
            currency_data[currency_label].columns = pd.to_datetime(
                currency_data[currency_label].columns)

    fig = go.Figure()
    for currency_label, price_data in currency_data.items():
        fig.add_trace(go.Scatter(x=price_data.columns, y=price_data.iloc[0],
                                 name=currency_label))

    fig.update_layout(title="Currency Trends",
                      xaxis_title="Date",
                      yaxis_title="Price")

    return fig
