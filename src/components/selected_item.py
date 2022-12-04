from dash import Dash, html
from dash.dependencies import Input, Output

from src.data.item_data import ItemData

from . import ids


def render(app: Dash, item_data: ItemData) -> html.Div:
    @app.callback(
        Output(ids.SELECTED_ITEM, "children"),
        Input(ids.ITEM_DATA_TABLE, "selected_row_ids"),
    )
    def update_selected_item(selected_row_ids: list[int]) -> html.H4:
        if selected_row_ids is None:
            return html.H4(
                id=ids.SELECTED_ITEM, children="Select a bid item from the table"
            )

        if selected_row_ids is not None:
            item = item_data.get_item_dict(selected_row_ids[0])
            item_number = (
                str(item.get("spec_code"))
                + "."
                + str(item.get("unit_code"))
                + "/"
                + str(item.get("item_code"))
            )
            item_description = item.get("short_description")
            return html.H4(
                id=ids.SELECTED_ITEM,
                children=f"Selected Item: {item_number} - {item_description}",
            )

    return html.Div(
        className="selected-item-container",
        children=html.H4(id=ids.SELECTED_ITEM),
    )
