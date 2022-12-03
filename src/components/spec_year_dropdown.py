from dash import Dash, dcc, html

from . import ids


def render(app: Dash) -> html.Div:
    all_spec_years = ["2020", "2018", "2016"]

    return html.Div(
        className="spec-dropdown",
        children=[
            html.Span(children="Select a Specification Year "),
            dcc.Dropdown(
                id=ids.SPEC_YEAR_DROPDOWN,
                options=all_spec_years,
                value=all_spec_years[0],
            ),
        ],
    )
