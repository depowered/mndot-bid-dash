import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dependencies import Input, Output, State

from src.data.bid_data import BidDataFactory

from . import (
    bid_scatter_plot,
    bid_summary_table,
    ids,
    bid_box_plot,
    bid_price_v_quanity,
)

_data_disclaimer = """The data provided by this application is for informational 
purposes only and is provided "as-is" without any warranty, express or implied. The data may 
not be complete, accurate, or up-to-date, and may be subject to change without notice. The 
data should not be used as the sole basis for making any decisions. Power Geospatial and any 
related parties shall not be held liable for any damages arising from or in connection with 
the use of the data provided."""


def render(app: Dash, bid_data_factory: BidDataFactory) -> html.Div:
    @app.callback(
        Output(ids.BID_ANALYTICS_CONTAINER, "children"),
        State(ids.ITEM_DATA_TABLE, "selected_row_ids"),
        Input(ids.SELECTED_ITEM_BUTTON, "n_clicks"),
    )
    def update_bid_data(
        selected_row_ids: list[str | int], selected_item_n_clicks: int
    ) -> html.Div:
        if selected_item_n_clicks < 1:
            return dash.no_update

        item_id = int(selected_row_ids[0])
        try:
            bid_data = bid_data_factory(item_id)
        except KeyError:
            return html.Div(
                style={"display": "flex", "justify-content": "center"},
                children=dbc.Alert(
                    "No bids exist for the selected item. Please try another.",
                    color="danger",
                ),
            )

        summary_table = bid_summary_table.render(app, bid_data)
        scatter_plot = bid_scatter_plot.render(app, bid_data)
        box_plot = bid_box_plot.render(app, bid_data)
        price_v_quantity = bid_price_v_quanity.render(app, bid_data)

        return html.Div(
            id=ids.BID_ANALYTICS,
            children=[
                dbc.Tabs(
                    id=ids.BID_ANALYTICS_TABS,
                    children=[
                        dbc.Tab(label="Bid Summary Table", children=summary_table),
                        dbc.Tab(label="Box Plot by Year", children=box_plot),
                        dbc.Tab(label="Unit Price vs Time", children=scatter_plot),
                        dbc.Tab(
                            label="Unit Price vs Quantity", children=price_v_quantity
                        ),
                    ],
                    active_tab="tab-0",
                ),
                html.Div(
                    id=ids.DISCLAIMER,
                    children=[
                        html.Strong("Disclaimer:  "),
                        html.Span(_data_disclaimer),
                    ],
                ),
            ],
        )

    return html.Div(id=ids.BID_ANALYTICS, children=None)
