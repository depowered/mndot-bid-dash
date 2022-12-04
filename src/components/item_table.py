from dash import Dash, dash_table, html
from dash.dependencies import Input, Output

from src.data.item_data import ItemData

from . import ids

columns = [
    {"id": "Item Number", "name": "Item Number"},
    {"id": "Short Description", "name": "Short Description"},
    {"id": "Long Description", "name": "Long Description"},
    {"id": "Unit Name", "name": "Unit Name"},
    {"id": "Plan Unit Description", "name": "Plan Unit Description"},
    {"id": "Spec Year", "name": "Spec Year"},
]


style_cell = {
    "textAlign": "left",
    "fontSize": "16px",
    "padding-right": "5px",
    "padding-left": "5px",
}

style_header = {
    "backgroundColor": "black",
    "fontWeight": "bold",
    "color": "white",
    "padding-right": "5px",
    "padding-left": "5px",
}

row_selectable = "single"


def render(app: Dash, item_data: ItemData) -> html.Div:

    blank_item_data_table = dash_table.DataTable(
        id=ids.ITEM_DATA_TABLE,
        data=[],
        columns=columns,
        style_cell=style_cell,
        style_header=style_header,
        row_selectable=row_selectable,
    )

    @app.callback(
        Output(ids.ITEM_DATA_TABLE_CONTAINER, "children"),
        Input(ids.SPEC_YEAR_DROPDOWN, "value"),
    )
    def update_data_table(spec_year: str) -> dash_table.DataTable:
        if spec_year == "":
            return blank_item_data_table

        item_data_table = dash_table.DataTable(
            id=ids.ITEM_DATA_TABLE,
            data=item_data.get_item_table_data(spec_year),
            columns=columns,
            page_size=20,
            style_cell=style_cell,
            style_header=style_header,
            row_selectable=row_selectable,
        )

        return item_data_table

    return html.Div(id=ids.ITEM_DATA_TABLE_CONTAINER)
