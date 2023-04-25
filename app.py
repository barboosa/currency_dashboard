import dash
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from pages import correlations, trends

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = "Currency Dashboard"

app.layout = dbc.Row([
    dbc.NavbarSimple(
        children=[
            dcc.Location(id='url', refresh=False),
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Trends", href="/trends")),
            dbc.NavItem(dbc.NavLink("Correlation", href="/correlation")),
        ],
        brand="Currency Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
    ),
    dbc.Container(id='page-content')
])

home_layout = dbc.Container([
    html.H1("Home")
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/trends':
        return trends.trends_layout
    elif pathname == '/correlation':
        return correlations.correlations_layout
    else:
        return home_layout


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True)