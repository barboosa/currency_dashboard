from pages import home, trends, correlations
from dash import Input, Output, dcc, html, Dash
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Currencies Dashboard'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Trends", href="/trends")),
        dbc.NavItem(dbc.NavLink("Correlations", href="/correlations")),
    ],
    brand="Currencies Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content")
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/trends":
        return trends.layout
    elif pathname == "/correlations":
        return correlations.layout
    elif pathname == "/":
        return home.layout
    else:
        return html.H1('404 - Page not found', style={'textAlign': 'center'}, className='text-danger mt-5')


if __name__ == '__main__':
    app.run_server(debug=True)
