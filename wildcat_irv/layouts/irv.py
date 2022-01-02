from typing import Any
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
from wildcat_connection.utils import ParsingException

from wildcat_irv.app import app
from wildcat_irv.layouts.table import get_styled_table
from wildcat_irv.layouts.stores import RawResults, IRVElectionResults

CSV_ENDING = '.csv'

layout = [
    dbc.Row(
        id='irv-info-row',
        children=[
            dbc.Col(
                dcc.Link(html.H4("About"), href='/about'),
                width=1),
            dbc.Col(
                dcc.Link(html.H4("Setting up IRV Election"), href='/instructions'),
                width=2)
        ],
        justify='end',
        align='end',
        style={
            'margin-top': '15px'
        }
    ),
    dbc.Row(
        id='irv-title',
        children=dbc.Col(html.H2("Wildcat Connection IRV")),
        style={
            "padding": "10% 0 0 0"
        },
        align='end'
    ),
    dbc.Row(dbc.Col(dcc.Upload(
        id='upload-wc-csv',
        children=html.Div(
            html.Button(
                children="Upload Wildcat Connection Election",
                className='raise',
                style={'width': '100%', 'height': '60px', 'margin': '10px'}
            )
        )
    ), width=6), justify='center'),
    dbc.Row(dbc.Col(
        html.Div(id='winner-table-div',
                 style={'width': '100%',
                        'padding': '0 2em'}),
        width=6
    ), justify='center'),
    dbc.Row([
        dbc.Col(dcc.Link(
            html.Button(
                "IRV computation steps",
                hidden=True,
                style={'width': '100%'},
                id='steps-link-button'
            ),
            href='/steps'
        ), style={'display': 'inline'}, width=3),
        dbc.Col(dcc.Link(
            html.Button(
                "Anonymized Ballots",
                hidden=True,
                style={'width': '100%'},
                id='ballots-link-button'
            ), href='/ballots'
        ), style={'display': 'inline'}, width=3)
    ], justify='center')
]

about_model = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("About")),
        dbc.ModalBody()
    ]
)


@app.callback(
    Output('winner-table-div', 'children'),
    Output('irv-results-store', 'data'),
    Output('irv-ballots-store', 'data'),
    Input('upload-wc-csv', 'filename'),
    State('upload-wc-csv', 'contents'),
    State('irv-results-store', 'data')
)
def handle_file_upload(
    filename: str,
    contents: str,
    cached_results_data: RawResults
) -> tuple[Any, dict, dict]:
    """Computes winner from Wildcat Connection Election"""
    if filename is None:
        return dash.no_update, dash.no_update, dash.no_update  # noqa
    if not filename.endswith(CSV_ENDING):
        return "Incorrect filetype passed!", {}, {}  # noqa
    # TODO: If slowness is a problem, then do not write to a tempfile.
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(decoded)
        tfile.seek(0)
        try:
            ballot = WildcatConnectionCSV(tfile)
        except ParsingException as e:
            return html.Div(
                dcc.Markdown(str(e)),
                style={
                    'border-style': 'solid',
                    'border-width': '1px',
                    'margin': '10px',
                    'width': '100%',
                    'padding': '10px 2em'
                }
            ), {}, {}

    # Generate Ballot lists and results
    results = {}
    ballots = {}
    for name, ballot_str in ballot.question_formatted_ballots.items():
        election = IRVElection(StringIO(ballot_str), name)
        winner, steps = election.run()
        results[name] = (winner, steps)
        ballots[name] = election.ballots.tolist()

    # Make Results Table
    data = []
    for election, (winner, _) in results.items():
        data.append({"Election": election, "Winner": winner, "# of Valid Votes": len(ballots[election])})
    columns = [{'name': "Election", 'id': "Election"},
               {'name': "Winner", 'id': "Winner"},
               {'name': "# of Valid Votes", 'id': "# of Valid Votes"}]
    table = get_styled_table(data, columns, sort_filter=False)
    return table, results, ballots


@app.callback(
    Output('steps-link-button', 'hidden'),
    Output('ballots-link-button', 'hidden'),
    Input('irv-results-store', 'data')
)
def show_buttons(data: tuple) -> tuple[bool, bool]:
    if not data:
        return True, True
    else:
        return False, False

