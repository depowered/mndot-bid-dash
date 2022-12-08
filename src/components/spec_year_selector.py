import dash_bootstrap_components as dbc

from . import ids


def render() -> dbc.RadioItems:

    radio_items = dbc.RadioItems(
        id=ids.SPEC_YEAR_SELECTOR,
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-primary",
        labelCheckedClassName="active",
        options=[
            {"label": "Spec Year 2020", "value": "2020"},
            {"label": "Spec Year 2018", "value": "2018"},
            {"label": "Spec Year 2016", "value": "2016"},
        ],
        value="2020",
    )

    return radio_items
