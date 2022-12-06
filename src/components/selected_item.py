import dash
from dash import Dash, html
from dash.dependencies import Input, Output

from src.data.item_data import ItemData

from . import ids


def render(app: Dash, item_data: ItemData) -> html.Button:
    @app.callback(
        Output(ids.SELECTED_ITEM_CONTAINER, "children"),
        Input(ids.ITEM_DATA_TABLE, "selected_row_ids"),
    )
    def update_button_text(selected_row_ids: list[str]) -> html.Button:
        if selected_row_ids is None:
            return dash.no_update

        item_id = int(selected_row_ids[0])
        item = item_data.get_item_dict(item_id)
        item_number = (
            str(item.get("spec_code"))
            + "."
            + str(item.get("unit_code"))
            + "/"
            + str(item.get("item_code"))
        )
        item_description = item.get("short_description")

        return html.Button(
            id=ids.SELECTED_ITEM_BUTTON,
            children=[
                html.Span("View Bid Data For:"),
                html.Span(f"{item_number} - {item_description}"),
            ],
            n_clicks=0,
            # style={"display": "grid"},
        )

    return html.Button(
        id=ids.SELECTED_ITEM_BUTTON,
        children="Select an item",
        n_clicks=0,
        # style={"display": "none"},
    )
