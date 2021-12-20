import dash
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
from dash.dash_table import DataTable


from wildcat_irv.app import app
from wildcat_irv.layouts.stores import IRVElectionResults
from wildcat_irv.layouts.table import get_styled_table

RawResults = dict[str, tuple[str, list[dict]]]

layout = [
    dbc.Row([
        dbc.Col(dcc.Link(html.Div("Back", className='centerBlock'), href='/election'), width=3),
        dbc.Col(html.H1("Instant Runoff Voting Steps"), width=6)
    ], justify='start', align='center'),
    dbc.Row([
        dbc.Col(html.H4("Election: "), width=1),
        dbc.Col(dcc.Dropdown(id='steps-election-dropdown'), width=2),
        dbc.Col(
            html.Img(
                id='steps-left-arrow',
                src='assets/img/next.png',
                className='flip-horizontally',
                style={
                    'height': '50px',
                    'width': '50px',
                    'top': '20px'
                }
            ),
            width=1
        ),
        dbc.Col(
            [html.H2(1, id='step-number'),
             dcc.Store(id='max-step-num', data=0)],
            width=1
        ),
        dbc.Col(html.Img(
            id='steps-right-arrow',
            src='assets/img/next.png',
            style={
                'height': '50px',
                'width': '50px',
                'top': '20px'
            }
        ), width=1)
    ], justify='left', align='center', style={'margin': '0'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                id='steps-bar-chart-div',
                style={
                    'width': '80%',
                    'display': 'inline-block',
                    'border-style': 'solid',
                    'border-width': '1px',
                    'border-color': 'white'
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Center([
                html.H2("Current Ballot"),
                html.Div(id='steps-data-table-div')
            ], style={
                'width': '90%',
                'border-style': 'solid',
                'border-width': '1px',
                'border-color': 'white'
            }
            ),
            width=6,
            align='top'
        )
    ]),
]


@app.callback(
    Output('steps-election-dropdown', 'options'),
    Output('steps-election-dropdown', 'value'),
    Input('irv-results-store', 'data')
)
def populate_dropdown_options(results_data: RawResults) -> tuple[list[dict[str, str]], str]:
    if not results_data:
        return [], dash.no_update
    results = IRVElectionResults(results_data)
    election_names = results.winners.keys()
    return [
        {'label': election, 'value': election}
        for election in election_names
    ], next(iter(election_names))


@app.callback(
    Output('max-step-num', 'data'),
    Input('steps-election-dropdown', 'value'),
    State('irv-results-store', 'data')
)
def populate_step_selector(election_selected: str, results_data: RawResults) -> int:
    if not results_data:
        return 0
    results = IRVElectionResults(results_data)
    num_steps = len(results.steps[election_selected])
    return num_steps


@app.callback(
    Output('step-number', 'children'),
    Output('steps-left-arrow', 'hidden'),
    Output('steps-right-arrow', 'hidden'),
    Input('steps-left-arrow', 'n_clicks'),
    Input('steps-right-arrow', 'n_clicks'),
    Input('max-step-num', 'data'),
    State('step-number', 'children')
)
def update_num_step(
    left_clicks: int, right_clicks: int, max_step_num: int,  # noqa
    step_number: int
) -> tuple[int, bool, bool]:
    step_number = int(step_number)
    triggered = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered == 'steps-left-arrow':
        step_number = step_number - 1
    elif triggered == 'steps-right-arrow':
        step_number = step_number + 1
    elif triggered == 'max-step-num':
        step_number = 1

    left_hidden, right_hidden = False, False
    if step_number == 1:
        left_hidden = True
    if step_number >= int(max_step_num):
        right_hidden = True
    return step_number, left_hidden, right_hidden


@app.callback(
    Output('steps-bar-chart-div', 'children'),
    Input('step-number', 'children'),
    State('steps-election-dropdown', 'value'),
    State('irv-results-store', 'data')
)
def populate_bar_chart(
    step_num: str, selected_election: str, results_data: RawResults
) -> dcc.Graph:
    if not results_data:
        return dash.no_update
    step_num = int(step_num)
    results = IRVElectionResults(results_data)

    step = results.steps[selected_election][step_num-1]
    candidates, values = [], []
    for c, v in step.items():
        candidates.append(c)
        values.append(v)

    figure = go.Figure([
        go.Bar(x=candidates, y=values)
    ])

    figure.update_layout(
        xaxis_title='Candidates',
        yaxis_title='Number of First Place Votes',
        title_text="Current First Place Vote Tallies",
        template='plotly_dark'
    )
    return dcc.Graph(
        figure=figure
    )


@app.callback(
    Output('steps-data-table-div', 'children'),
    Input('step-number', 'children'),
    State('steps-election-dropdown', 'value'),
    State('irv-results-store', 'data'),
    State('irv-ballots-store', 'data')
)
def populate_data_table(
    step_num: str, selected_election: str,
    results_data: RawResults, ballot_data: dict[str, list[list[str]]]
) -> DataTable:
    if not ballot_data:
        return dash.no_update
    results = IRVElectionResults(results_data)
    step_num = int(step_num)
    remaining_candidates = set(results.steps[selected_election][step_num-1].keys())
    election_ballot_data = ballot_data[selected_election]
    table_data = []
    for row in election_ballot_data:
        row = [c if c in remaining_candidates else None
               for c in row]
        table_data.append({str(i): vote for i, vote in enumerate(row, start=1)})
    columns = [{"name": f"Choice {i}", "id": str(i)}
               for i in range(1, len(table_data[0]) + 1)]

    table = get_styled_table(table_data, columns)
    return table
