import requests
import datetime
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime as dt
from dash import dcc, html, Input, Output, callback, Dash, exceptions
import dash_bootstrap_components as dbc


def fetch_currency_data():
    currency_data = requests.get('http://127.0.0.1:8000/currencies').json()
    currency_options = [{'label': currency.replace(
        '=X', ''), 'value': currency} for currency in currency_data]
    return currency_options


def fetch_historic_events_data():
    historic_events_data = requests.get(
        'http://127.0.0.1:8000/historic-events').json()
    historic_event_options = [{'label': event['eventName'],
                               'value': event['date']} for event in historic_events_data]
    return historic_event_options


def convert_to_date(input_date):
    return dt.strptime(input_date.split('T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')


def fetch_and_format_currency_data(start_date, end_date, selected_currencies):
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
    return currency_data


def generate_figure(currency_data, start_date, end_date):
    fig = go.Figure()
    for currency_label, price_data in currency_data.items():
        fig.add_trace(go.Scatter(x=price_data.index,
                      y=price_data[currency_label], name=currency_label))
    fig.update_layout(title=f"Currency Trends Over Time (Data from {start_date} to {end_date})",
                      xaxis_title="Date", yaxis_title="Normalized Price")
    return fig


currency_options = fetch_currency_data()
historic_event_options = fetch_historic_events_data()

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.H5("Select Date Range:"), width=3),
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='date-picker',
                            min_date_allowed=datetime.datetime(1980, 1, 1),
                            max_date_allowed=datetime.datetime.now() - datetime.timedelta(days=1),
                            start_date=datetime.datetime.now() - datetime.timedelta(days=120),
                            end_date=datetime.datetime.now() - datetime.timedelta(days=1),
                        ), width=9),
                ])
            ], className='dcc_control'),
        ], width=6),

        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.H5("Select Historic Event:"), width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='event-selector',
                            options=historic_event_options,
                            multi=False
                        ), width=9),
                ])
            ], className='dcc_control'),
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.H5("Select Currencies:"), width=2),
                    dbc.Col(
                        dcc.Dropdown(
                            id='currency-selector',
                            options=currency_options,
                            value=[currency['value']
                                   for currency in currency_options],
                            multi=True
                        ), width=10),
                ])
            ], className='dcc_control'),
        ], width=12),
    ]),

    dbc.Row([
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


@callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    [Input('event-selector', 'value')]
)
def update_datepicker(historic_event_date):
    if historic_event_date is None:
        raise exceptions.PreventUpdate
    else:
        historic_event_date = dt.strptime(historic_event_date, '%Y-%m-%d')
        end_date = historic_event_date + datetime.timedelta(days=120)
        return historic_event_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


@callback(
    Output('currency-trends-graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('currency-selector', 'value')]
)
def update_graph(start_date, end_date, selected_currencies):
    start_date = convert_to_date(start_date)
    end_date = convert_to_date(end_date)

    currency_data = fetch_and_format_currency_data(
        start_date, end_date, selected_currencies)

    return generate_figure(currency_data, start_date, end_date)
