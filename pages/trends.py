import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

currency = "CHF=X"
start_date = "2017-01-01"
end_date = "2022-12-31"

data = yf.download(currency, start=start_date, end=end_date)

trends_layout = dbc.Container([
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='currency_trend_chart',
            figure={
                'data': [
                    go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Currency Trend')
                ],
                'layout': go.Layout(title=f'Currency Trend')
            }
        )
    )),
])