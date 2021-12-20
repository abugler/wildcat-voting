from typing import Any

from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

from wildcat_irv.layouts.table import get_styled_table

NUM_TABLE_COLUMNS = 3

layout = html.Div(id='ballot-layout-div')

HEADER_ROW = dbc.Row([
    dbc.Col(dcc.Link(html.Div("Back", className='centerBlock'), href='/election'), width=3),
    dbc.Col(html.H1("Instant Runoff Voting Ballots"), width=6)
], justify='start', align='center')

def populate_table(data: dict[list[list[str]]]) -> Any:
    """
    Populates the loading table with anonymized data.

    Called by `display_page` in index.
    
    Because of the necessity of having JSON serializable data in Store
    objects, the data structure for 'irv-results-store' is a mess.
    """
    if not data:
        return [HEADER_ROW, dbc.Row(dbc.Col("Please upload a WC csv first"))]

    ballot_columns = [
        dbc.Col(
            html.Div(
                children=[
                    html.H2(election_name),
                    get_styled_table(
                        data=[{str(i): vote for i, vote in enumerate(row, start=1)} for row in ballot_data],
                        columns=[{"name": f"Choice {i}", "id": str(i)}
                                 for i in range(1, len(ballot_data[0]) + 1)],
                    )
                ]
            )
        , width=12 // NUM_TABLE_COLUMNS,
            style={
                'width': f'{100 // NUM_TABLE_COLUMNS}%',
                'display': 'inline-block',
                'align': 'center'
            }
        )
        for election_name, ballot_data in data.items()
    ]

    rows = [
        dbc.Row(children=ballot_columns[idx:idx+NUM_TABLE_COLUMNS])
        for idx in range(0, len(ballot_columns), NUM_TABLE_COLUMNS)
    ]
    rows.insert(0, HEADER_ROW)
    return rows


