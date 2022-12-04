from typing import Callable

from dash import Dash, html, dash_table
from dash.dependencies import Input, Output

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


def render(app: Dash, item_loader_func: Callable) -> html.Div:
    @app.callback(
        Output(ids.ITEM_DATA_TABLE_CONTAINER, "children"),
        Input(ids.SPEC_YEAR_DROPDOWN, "value"),
    )
    def update_data_table(spec_year: str) -> dash_table.DataTable:
        df = item_loader_func(spec_year)

        item_data_table = dash_table.DataTable(
            id=ids.ITEM_DATA_TABLE,
            data=df.to_dict("records"),
            columns=columns,
            page_size=20,
            style_cell=style_cell,
            style_header=style_header,
            row_selectable=row_selectable,
        )

        return item_data_table

    blank_item_data_table = dash_table.DataTable(
        id=ids.ITEM_DATA_TABLE,
        data=[],
        columns=columns,
        style_cell=style_cell,
        style_header=style_header,
        row_selectable=row_selectable,
    )

    return html.Div(id=ids.ITEM_DATA_TABLE_CONTAINER, children=blank_item_data_table)
