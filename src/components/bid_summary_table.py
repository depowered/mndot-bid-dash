from dash import Dash, dash_table

from src.data.bid_data import BidData

from . import ids


def _create_data_table(bid_data: BidData) -> dash_table.DataTable:
    df = bid_data.summary_table_df()
    data = df.to_dict(orient="records")

    columns = [{"name": i, "id": i} for i in df.columns]

    style_cell = {
        "background-color": "rgb(68, 68, 68)",
        "border": "1px solid rgb(87, 87, 87)",
        "text-align": "center",
        "font-size": "16px",
        "font-family": "var(--bs-body-font-family)",
        "padding-right": "5px",
        "padding-left": "5px",
    }

    style_header = {
        "background-color": "black",
        "border": "1px solid rgb(87, 87, 87)",
        "text-align": "center",
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

    row_selectable = False
    page_size = 20

    return dash_table.DataTable(
        id=ids.BID_SUMMARY_TABLE,
        data=data,
        columns=columns,
        page_size=page_size,
        style_cell=style_cell,
        style_header=style_header,
        row_selectable=row_selectable,
        style_data_conditional=style_data_conditional,
        cell_selectable=False,
    )


def render(app: Dash, bid_data: BidData) -> dash_table.DataTable:
    return _create_data_table(bid_data)
