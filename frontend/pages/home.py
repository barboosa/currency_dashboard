from dash import html
import dash_bootstrap_components as dbc

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
            html.P("Libraries used:",
                   className="text-center mt-5 mb-3 font-weight-bold"),
            html.Ul([
                html.Li(
                    "Dash - A productive Python framework for building web applications"),
                html.Li("Plotly - An open-source graphing library for Python"),
                html.Li(
                    "Pandas - A powerful data manipulation and analysis library"),
                html.Li(
                    "Requests - A versatile HTTP library for making API requests"),
                html.Li("Datetime - A module for working with dates and times")
            ], className="list-unstyled text-muted text-center")
        ], className="mt-5")
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Thank you to the used libraries for their valuable contributions:",
                   className="text-center mt-5 text-muted")
        ])
    ])
], className="mt-5")
