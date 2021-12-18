from dash import html
from dash import dcc

footer = html.Div([
    "Made for the ",
    dcc.Link("Slivka Residential College of Science and Engineering at Northwestern University",
             href="http://slivka.northwestern.edu/", style={'text-decoration': 'none'}),
    html.Br(),
], style={
    'bottom': '0px',
    'left': '0px',
    'position': 'fixed',
    'width': '765px',
    'margin-bottom': '20px'
}
)
