from dash import dcc

from . import classes, ids


def render() -> dcc.RadioItems:

    radio_items = dcc.RadioItems(
        id=ids.SPEC_YEAR_SELECTOR,
        labelClassName=classes.SPEC_YEAR_SELECTOR_ITEM,
        options=[
            {"label": "Spec Year 2020", "value": "2020"},
            {"label": "Spec Year 2018", "value": "2018"},
            {"label": "Spec Year 2016", "value": "2016"},
        ],
        value="2020",
    )

    return radio_items
