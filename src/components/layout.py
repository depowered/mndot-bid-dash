from dash import Dash, html

from . import spec_year_dropdown, item_table
from ..data.item_loader import load_item_table_df


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[spec_year_dropdown.render(app)],
            ),
            item_table.render(app, load_item_table_df),
        ],
    )
