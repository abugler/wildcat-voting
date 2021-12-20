# Run this wildcat_irv with `python wildcat_irv.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from wildcat_irv.layouts import footer, stores

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    stores.get_stores(),
    dbc.Container(
        id='page-content',
        style={
            'justify-content': 'center',
            'align-items': 'center',
            'height': '100%'
        },
        fluid=True,
    ),
    footer.footer,
],
    style={
        'height': '100vh',
        'width': '100vw',
    }
)
