from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.item_data import ItemData


def main() -> None:

    item_data = ItemData()

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "MnDOT Bid Prices Dashboard"
    app.layout = create_layout(app, item_data)
    app.run()
    # app.run(dev_tools_hot_reload=True)


if __name__ == "__main__":
    main()
