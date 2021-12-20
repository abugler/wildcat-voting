from dash.dash_table import DataTable


def get_styled_table(data, columns, sort_filter=True, **kwargs) -> DataTable:
    return DataTable(
        data=data,
        columns=columns,
        style_header={
            'backgroundColor': '#836EAA'
        },
        style_data={
            'backgroundColor': '#716C6B',
            'height': 'auto'
        },
        style_cell={
            'textAlign': 'left'
        },
        editable=False,
        sort_action='native' if sort_filter else 'none',
        filter_action='native' if sort_filter else 'none',
        fill_width=True,
        **kwargs
    )