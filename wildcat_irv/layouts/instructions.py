from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pathlib

with open(pathlib.Path(__file__).parent.parent / 'assets/setting_up_election.md') as f:
    instructions_md_text = f.read()


layout = [
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                instructions_md_text,
                style={
                    'text-align': 'left'
                }
            ), width=7
        ),
        dbc.Col(
            [
                html.P(
                    "Election Creation Page",
                    style={
                        'margin': '5px'
                    }
                ),
                html.Img(
                    src='assets/img/img1.png',
                    style={
                        'max-width': '750px'
                    }
                ),
                html.P(
                    "Question Creation Page",
                    style={
                        'margin': '5px'
                    }
                ),
                html.Img(
                    src='assets/img/img3.png',
                    style={
                        'max-width': '750px'
                    }
                )
            ]
        )
    ], justify='center'),
    dbc.Row(dbc.Col(
        dcc.Link(dbc.Button("Back"), href='/election')
    ))
]