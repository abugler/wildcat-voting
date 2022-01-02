from dash import dcc
import dash_bootstrap_components as dbc
import pathlib

with open(pathlib.Path(__file__).parent.parent / 'assets/about.md') as f:
    about_md_text = f.read()


layout = [
    dbc.Row(dbc.Col(
        dcc.Markdown(about_md_text), width=6
    ), justify='center', style={'margin-top': '10%'}),
    dbc.Row(dbc.Col(
        dcc.Link(dbc.Button("Back"), href='/election')
    ))
]