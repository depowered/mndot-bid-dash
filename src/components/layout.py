from dash import Dash, html

from . import classes, ids, item_search, item_table, selected_item, spec_year_selector


def create_layout(app: Dash, item_data) -> html.Div:
    return html.Div(
        className=classes.APP_DIV,
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                id=ids.SPEC_YEAR_SELECTOR_CONTAINER,
                children=spec_year_selector.render(),
            ),
            html.Div(id=ids.ITEM_SEARCH_CONTAINER, children=item_search.render()),
            html.Div(
                id=ids.ITEM_DATA_TABLE_CONTAINER,
                children=item_table.render(app, item_data),
            ),
            html.Div(
                id=ids.SELECTED_ITEM_CONTAINER,
                children=selected_item.render(app, item_data),
            ),
        ],
    )
