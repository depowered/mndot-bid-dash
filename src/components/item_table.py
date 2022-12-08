from dash import Dash, State, ctx, dash_table, html, no_update
from dash.dependencies import Input, Output

from src.data.item_data import ItemData, ItemTableData

from . import ids


def _create_data_table(data: ItemTableData) -> dash_table.DataTable:
    columns = [
        {"id": "Item Number", "name": "Item Number"},
        {"id": "Short Description", "name": "Short Description"},
        {"id": "Long Description", "name": "Long Description"},
        {"id": "Unit Name", "name": "Unit Name"},
        {"id": "Plan Unit Description", "name": "Plan Unit Description"},
        {"id": "Spec Year", "name": "Spec Year"},
    ]

    style_cell = {
        "background-color": "rgb(68, 68, 68)",
        "border": "1px solid rgb(87, 87, 87)",
        "text-align": "left",
        "font-size": "16px",
        "font-family": "var(--bs-body-font-family)",
        "padding-right": "5px",
        "padding-left": "5px",
    }

    style_header = {
        "background-color": "black",
        "border": "1px solid rgb(87, 87, 87)",
        "font-family": "var(--bs-body-font-family)",
        "font-weight": "bold",
        "color": "white",
        "padding-right": "5px",
        "padding-left": "5px",
    }

    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(54, 54, 54)",
        }
    ]

    row_selectable = "single"
    page_size = 20

    return dash_table.DataTable(
        id=ids.ITEM_DATA_TABLE,
        data=data,
        columns=columns,
        page_size=page_size,
        style_cell=style_cell,
        style_header=style_header,
        row_selectable=row_selectable,
        style_data_conditional=style_data_conditional,
        cell_selectable=False,
    )


def render(app: Dash, item_data: ItemData) -> html.Div:
    @app.callback(
        Output(ids.ITEM_DATA_TABLE_CONTAINER, "children"),
        State(ids.SPEC_YEAR_SELECTOR, "value"),
        State(ids.ITEM_SEARCH_INPUT, "value"),
        Input(ids.ITEM_SEARCH_BUTTON, "n_clicks"),
    )
    def update_data_table(
        spec_year: str, search_value: str, submit_n_clicks: int
    ) -> dash_table.DataTable:
        if ids.ITEM_SEARCH_BUTTON != ctx.triggered_id:
            return no_update

        data = item_data.query(spec_year, search_value)
        return html.Div(children=_create_data_table(data))

    return html.Div(children=None)
