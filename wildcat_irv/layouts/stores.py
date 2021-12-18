from dash import html
from dash import dcc

store_irv_results = dcc.Store(id='irv-results-store')
store_irv_ballot = dcc.Store(id='irv-ballots-store')


class IRVElectionResults:
    """
    Contains the output of election results. This converts the JSON serializable
    list of tuples into a more readable format.

    Parameters
    ----------
    results : dict[str, tuple[str, list[dict]]]
        The output of `irv.__main__.run`, where item in the dict is an election name
        mapped to a two tuple of `winner` and `steps`.

    Attributes
    ----------
    winners :  dict[str, str]
        Maps election name to winner
    steps : dict[str, list[dict]]
        Maps election name to election steps
    """
    def __init__(self, results: dict[str, tuple[str, list[dict]]]):
        self.winners = {}
        self.steps = {}
        for election, (winner, steps) in results.items():
            self.winners[election] = winner
            self.steps[election] = steps


def get_stores() -> html.Div:
    return html.Div(
        [store_irv_results, store_irv_ballot],
        id='store-div')
