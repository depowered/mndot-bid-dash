import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask

from src.components.layout import create_layout
from src.data.bid_data import BidDataFactory
from src.data.contract_data import ContractData
from src.data.item_data import ItemData


def configure_app() -> tuple[Dash, Flask]:

    item_data = ItemData()
    contract_data = ContractData()
    bid_data_factory = BidDataFactory(item_data, contract_data)

    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    app.title = "MnDOT Bid Prices Dashboard"
    app.layout = create_layout(app, item_data, bid_data_factory)

    return (app, app.server)


app, server = configure_app()

if __name__ == "__main__":
    app.run()
