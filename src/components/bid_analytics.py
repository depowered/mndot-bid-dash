import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dependencies import Input, Output, State

from src.data.bid_data import BidDataFactory

from . import bid_mean_plot, bid_scatter_plot, bid_summary_table, ids


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
        bid_data = bid_data_factory(item_id)
        summary_table = bid_summary_table.render(app, bid_data)
        scatter_plot = bid_scatter_plot.render(app, bid_data)
        mean_plot = bid_mean_plot.render(app, bid_data)

        return html.Div(
            id=ids.BID_ANALYTICS,
            children=[
                dbc.Tabs(
                    id=ids.BID_ANALYTICS_TABS,
                    children=[
                        dbc.Tab(label="Bid Summary Table", children=summary_table),
                        dbc.Tab(label="Average Unit Price", children=mean_plot),
                        dbc.Tab(label="Unit Price vs Time", children=scatter_plot),
                    ],
                    active_tab="tab-0",
                )
            ],
        )

    return html.Div(id=ids.BID_ANALYTICS, children=None)
