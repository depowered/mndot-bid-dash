import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dependencies import Input, Output

from src.data.item_data import ItemData

from . import ids


def render(app: Dash, item_data: ItemData) -> dbc.Button:
    @app.callback(
        Output(ids.SELECTED_ITEM_CONTAINER, "children"),
        Input(ids.ITEM_DATA_TABLE, "selected_row_ids"),
    )
    def update_button_text(selected_row_ids: list[str]) -> dbc.Button:
        if selected_row_ids is None:
            return dbc.Button(
                id=ids.SELECTED_ITEM_BUTTON,
                children="Select an item using the buttons in the left-most table column",
                n_clicks=0,
                disabled=True,
            )

        item_id = int(selected_row_ids[0])
        item = item_data.get_item_dict(item_id)
        item_number = item["Item Number"]
        item_description = item["Short Description"]

        return dbc.Button(
            id=ids.SELECTED_ITEM_BUTTON,
            children=[
                html.Span("View Bid Data For:"),
                html.Span(f"{item_number} - {item_description}"),
            ],
            n_clicks=0,
            outline=False,
        )

    return html.Div(children=None)
