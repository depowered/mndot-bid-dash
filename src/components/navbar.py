import dash_bootstrap_components as dbc


def render() -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    "API Docs",
                    href="https://mndotbidprices.com/api/v1/docs",
                    target="_blank",
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    "Power Geospatial",
                    href="https://www.powergeospatial.xyz/",
                    target="_blank",
                )
            ),
        ],
        brand="MnDOT Bid Prices Dashboard",
        color="primary",
        dark=True,
    )
