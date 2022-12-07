import plotly.express as px
from dash import Dash, dcc, html

from src.data.bid_data import BidData

from . import ids


def render(app: Dash, bid_data: BidData) -> html.Div:
    fig = px.scatter(
        bid_data.bid_figure_df,
        x="Letting Date",
        y="Unit Price",
        color="Bid Type",
        symbol="Bid Type",
        template="plotly_dark",
    )
    graph = dcc.Graph(id=ids.BID_SCATTER_PLOT_GRAPH, figure=fig)
    return html.Div(id=ids.BID_SCATTER_PLOT, children=graph)
