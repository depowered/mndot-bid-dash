import plotly.express as px
from dash import Dash, dcc, html

from src.data.bid_data import BidData

from . import ids


def render(app: Dash, bid_data: BidData) -> html.Div:
    fig = px.scatter(
        bid_data.bid_figure_df,
        x="Quantity",
        y="Unit Price",
        color="Bid Type",
        symbol="Bid Type",
        template="plotly_dark",
    )
    graph = dcc.Graph(figure=fig)
    return html.Div(children=graph)
