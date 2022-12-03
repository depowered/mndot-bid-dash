from dash import Dash, html

from . import spec_year_dropdown


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
        ],
    )
