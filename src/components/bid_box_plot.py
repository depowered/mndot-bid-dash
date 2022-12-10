import plotly.express as px
from dash import Dash, dcc, html

from src.data.bid_data import BidData

from . import ids


def render(app: Dash, bid_data: BidData) -> html.Div:
    fig = px.box(
        bid_data.box_plot_df(),
        x="Year",
        y="Unit Price",
        color="Bid Type",
        template="plotly_dark",
        category_orders={
            "Bid Type": ["Engineer", "Winning", "Losing"],
        },
    )
    graph = dcc.Graph(id=ids.BID_BOX_PLOT_GRAPH, figure=fig)
    return html.Div(id=ids.BID_BOX_PLOT, children=graph)
