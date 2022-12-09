import dash_bootstrap_components as dbc


def render() -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    "By Power Geospatial",
                    href="https://www.powergeospatial.xyz/",
                    target="_blank",
                )
            ),
        ],
        brand="MnDOT Bid Prices Dashboard",
        # brand_href="#",
        color="primary",
        dark=True,
    )
