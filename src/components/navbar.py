import dash_bootstrap_components as dbc


def render() -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("Power Geospatial", href="https://www.powergeospatial.xyz/")
            ),
        ],
        brand="MnDOT Bid Prices",
        brand_href="#",
        color="primary",
        dark=True,
    )
