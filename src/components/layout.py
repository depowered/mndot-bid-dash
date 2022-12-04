from dash import Dash, html

from . import item_table, selected_item, spec_year_dropdown


def create_layout(app: Dash, item_data) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[spec_year_dropdown.render(app)],
            ),
            item_table.render(app, item_data),
            selected_item.render(app, item_data),
        ],
    )
