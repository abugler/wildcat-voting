from io import StringIO
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import base64
import tempfile
from dash.dependencies import Output, Input, State

from irv import IRVElection
from wildcat_connection import WildcatConnectionCSV

from wildcat_irv.app import app

CSV_ENDING = '.csv'

layout = [
    dbc.Row(
        id='irv-header',
        children=dbc.Col(html.H2("Wildcat Connection IRV")),
        style={
            "padding": "15% 0 0 0"
        },
        align='end'
    ),
    dbc.Row(dcc.Upload(
        id='upload-wc-csv',
        children=html.Div(
            html.Button(
                children="Upload Wildcat Connection Election",
                className='raise',
                style={'width': '50%', 'height': '60px', 'margin': '10px'}
            )
        )
    )),
    dbc.Row(html.H3(id='winner-header', children='')),
    dbc.Row([
        dbc.Col(dcc.Link(
            html.Button(
                "IRV computation steps",
                style={'display': 'none'},
                id='steps-link-button'
            ),
            href='/steps'
        ), style={'display': 'inline'}, width=4),
        dbc.Col(dcc.Link(
            html.Button(
                "Anonymized Ballots",
                style={'display': 'none'},
                id='ballots-link-button'
            ), href='/ballots'
        ), style={'display': 'inline'}, width=4)
    ], justify='center')
]


@app.callback(
    Output('winner-header', 'children'),
    Output('irv-results-store', 'data'),
    Output('irv-ballots-store', 'data'),
    Input('upload-wc-csv', 'filename'),
    State('upload-wc-csv', 'contents'),
    State('upload-wc-csv', 'last_modified'),
    prevent_initial_call=True
)
def handle_file_upload(
    filename: str,
    contents: str,
    last_modified_timestamp: int
) -> tuple[list, dict, dict]:
    """Computes winner from Wildcat Connection Election"""
    if filename is None:
        return dash.no_update, dash.no_update, dash.no_update  # noqa
    if not filename.endswith(CSV_ENDING):
        return "Incorrect filetype passed!", list(), list()  # noqa
    # TODO: If slowness is a problem, then do not write to a tempfile.
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(decoded)
        tfile.seek(0)
        ballot = WildcatConnectionCSV(tfile)

    # Generate Ballot lists and results
    results = {}
    ballots = {}
    for name, ballot_str in ballot.question_formatted_ballots.items():
        election = IRVElection(StringIO(ballot_str), name)
        winner, steps = election.run()
        results[name] = (winner, steps)
        ballots[name] = election.ballots.tolist()

    # Make Results String
    result_string = []
    for election, (winner, steps) in results.items():
        result_string.append(f"Election: {election} | Winner: {winner}")
        result_string.append(html.Br())
    return result_string, results, ballots


@app.callback(
    Output('steps-link-button', 'style'),
    Output('ballots-link-button', 'style'),
    Input('irv-results-store', 'data'),
    prevent_initial_call=True
)
def show_buttons(data: tuple) -> tuple[dict[str, str], dict[str, str]]:
    if not data:
        return {'display': 'none'}, {'display': 'none'}
    else:
        return {'display': 'inline'}, {'display': 'inline'}
