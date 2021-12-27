import dash_bootstrap_components as dbc
from dash import html

layout = [
    dbc.Row(
        dbc.Col(
            html.H1(
                "When the spoiler effect is sus!",
                style={'margin-top': '20px'}
            )
        )
    ),
    dbc.Row(
        dbc.Col(html.Img(src="assets/img/purple_crewmate.png"))
    )
]