import plotly.express as px
from dash import Dash, dcc, html

from src.data.bid_data import BidData

from . import ids


def render(app: Dash, bid_data: BidData) -> html.Div:
    fig = px.line(
        bid_data.mean_unit_price_by_year(),
        x="Year",
        y="Unit Price",
        color="Bid Type",
        symbol="Bid Type",
        template="plotly_dark",
    )
    graph = dcc.Graph(figure=fig)
    return html.Div(id=ids.BID_MEAN_PLOT, children=graph)
