from dash.dependencies import Output, Input, State

from wildcat_irv.app import app
from layouts import irv as layout_irv
from layouts.ballots import populate_table
from layouts.steps import layout as steps_layout


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              State('irv-ballots-store', 'data'))
def display_page(pathname, ballot_data):
    if pathname == '/election':
        return layout_irv.layout
    if pathname == '/ballots':
        return populate_table(ballot_data)
    if pathname == '/steps':
        return steps_layout


if __name__ == '__main__':
    app.run_server(debug=True)  # TODO: figure out how to detect prod.
