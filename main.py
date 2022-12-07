from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.bid_data import BidDataFactory
from src.data.contract_data import ContractData
from src.data.item_data import ItemData


def main() -> None:

    item_data = ItemData()
    contract_data = ContractData()
    bid_data_factory = BidDataFactory(item_data, contract_data)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "MnDOT Bid Prices Dashboard"
    app.layout = create_layout(app, item_data, bid_data_factory)
    app.run()
    # app.run(dev_tools_hot_reload=True)


if __name__ == "__main__":
    main()
