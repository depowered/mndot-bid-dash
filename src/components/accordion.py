from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

welcome_md = """
Welcome to the MnDOT Bid Prices Dashboard.

This application enables an interactive exploration of bid data published in 
MnDOT's Bid Letting Abstracts.

The data is organized by item and contains bids from most\*\* abstracts published since 2018.
Use the search feature below to find an item of interest and begin exploring the available data. 
If you need a suggestion to get started, most abstracts contain the item "EXCAVATION - COMMON". 
That item will provide plenty of data points to explore in the interactive graphs.

\*\* *Approximately 95% of the abstracts for any given year have been captured here. Those that have 
not been captured did not pass the automated extraction process and will be added manually at a 
later date.*

"""

usage_md = """
From [MnDOT's Abstracts landing page](https://www.dot.state.mn.us/bidlet/abstract.html):

"Because there have been three Spec Books (MnDOT's Standard Specifications For Construction) 
in effect in the last 15 years and because of "Special Items" used on specific projects, you 
should be cautious when attempting to relate data for Items and Item Numbers from one project 
to another."

The actual number of Spec Books in the last 15 years is up to five since September 2022. 
Minor and major aspects of the exact work a bid item describes from one Spec version to 
the next impacts the prices bid by contractors. Moreover, prices from one project to 
another will vary due to location, season, materials sortages, or any hundred other factors 
not accounted for here.

So a few ideas to keep in mind when using this application:
 - More data is just that: more data. It is ***not necessarily better*** data.
 - Past performance is ***not indicative*** of future results.
 - The whole of the available data represents an ***incomplete*** snapshot of historic bid lettings.

Full disclaimer will be displayed below all data analytics.

"""


def render(app: Dash) -> html.Div:
    return html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(dcc.Markdown(welcome_md), title="About"),
                dbc.AccordionItem(dcc.Markdown(usage_md), title="Usage"),
            ]
        )
    )
