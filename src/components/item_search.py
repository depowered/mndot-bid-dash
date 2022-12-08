import dash_bootstrap_components as dbc
from dash import html

from . import ids


def render() -> html.Div:

    search_field = dbc.Input(
        id=ids.ITEM_SEARCH_INPUT,
        type="search",
        placeholder="Search by Item Number or Description",
    )

    search_button = dbc.Button("Search", id=ids.ITEM_SEARCH_BUTTON, n_clicks=0)

    component = html.Div(
        className=ids.ITEM_SEARCH, children=[search_field, search_button]
    )

    return component
