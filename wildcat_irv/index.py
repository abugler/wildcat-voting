import os
from dash.dependencies import Output, Input, State

from wildcat_irv.app import app, server  # noqa
from wildcat_irv.layouts import irv as layout_irv
from wildcat_irv.layouts.ballots import populate_table
from wildcat_irv.layouts.steps import layout as steps_layout
from wildcat_irv.layouts.amongus import layout as sussy


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              State('irv-ballots-store', 'data'))
def display_page(pathname, ballot_data):
    if pathname == '/election' or pathname == '/':
        return layout_irv.layout
    if pathname == '/ballots':
        return populate_table(ballot_data)
    if pathname == '/steps':
        return steps_layout
    if pathname == '/amongus':
        return sussy


if __name__ == '__main__':
    debug = not os.environ.get("HEROKU_PRODUCTION", False)
    print(f"Debug: {debug}")
    app.run_server(debug=debug)
