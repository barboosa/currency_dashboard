from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests


def fetch_supported_countries():
    response = requests.get("http://127.0.0.1:8000/countries")
    return response.json()


def prepare_map_figure(supported_countries):
    country_codes = [country['countryAlpha3']
                     for country in supported_countries]
    hover_text = [
        f"{country['name']} ({country['currencyAlpha3']})" for country in supported_countries]

    map_figure = go.Figure(data=go.Choropleth(
        locations=country_codes,
        z=[1]*len(country_codes),
        text=hover_text,
        hoverinfo='text',
        colorscale='matter',
        showscale=False
    ))

    map_figure.update_layout(
        geo=dict(
            showframe=False
        ),
        autosize=True,
        dragmode=False,
        margin=dict(
            autoexpand=True,
            l=0,
            r=0,
            t=0,
            b=0
        ),
    )
    return map_figure


supported_countries = fetch_supported_countries()
map_figure = prepare_map_figure(supported_countries)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Currencies Dashboard",
                    className="display-4 text-center mt-5 mb-4"),
            html.P("A Dashboard for Analyzing Currency Trends and Correlations based on Historical Events.",
                   className="lead text-center mb-5")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Currency Trends", className="text-center mt-4"),
            html.P("Explore the trends of various currency pairs over time using the Currency Trends page.",
                   className="text-center")
        ], width=6, className="mt-5"),
        dbc.Col([
            html.H5("Currency Correlations", className="text-center mt-4"),
            html.P("Discover the correlations between different currency pairs using the Currency Correlations page.",
                   className="text-center")
        ], width=6, className="mt-5")
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Supported Countries:",
                    className="text-center mt-5 mb-3 font-weight-bold"),
        ], className="mt-5")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=map_figure, style={'height': '600px'}),
        ], style={'padding': '20px'})
    ]),
], className="mt-5")
