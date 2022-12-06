from dash import dcc, html

from . import ids


def render() -> html.Div:

    search_field = dcc.Input(
        id=ids.ITEM_SEARCH_INPUT,
        type="search",
        placeholder="Search by Item Number or Description",
    )

    submit = html.Button("Submit", id=ids.ITEM_SEARCH_BUTTON, n_clicks=0)

    component = html.Div(className=ids.ITEM_SEARCH, children=[search_field, submit])

    return component
