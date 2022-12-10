from dash import Dash, html

from src.data.bid_data import BidDataFactory
from src.data.item_data import ItemData

from . import (
    accordion,
    bid_analytics,
    classes,
    ids,
    item_search,
    item_table,
    navbar,
    selected_item,
    spec_year_selector,
)


def create_layout(
    app: Dash, item_data: ItemData, bid_data_factory: BidDataFactory
) -> html.Div:
    return html.Div(
        className=classes.APP_DIV,
        children=[
            navbar.render(),
            html.Div(id=ids.ACCORDION_CONTAINER, children=accordion.render(app)),
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
            html.Div(
                id=ids.BID_ANALYTICS_CONTAINER,
                children=bid_analytics.render(app, bid_data_factory),
            ),
        ],
    )
