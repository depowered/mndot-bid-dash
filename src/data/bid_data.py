from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd

from .bid_loader import BidFigureDF, load_bid_figure_df
from .contract_data import ContractData
from .item_data import ItemData


@dataclass
class BidDataFactory:
    item_data: ItemData
    contract_data: ContractData

    def __call__(self, item_id: int) -> BidData:
        bid_figure_df = load_bid_figure_df(item_id, self.item_data, self.contract_data)
        return BidData(item_id, bid_figure_df)


@dataclass
class BidData:
    item_id: int
    bid_figure_df: BidFigureDF

    def filter_by_bid_type(self, bid_type: str) -> BidFigureDF:
        mask = self.bid_figure_df["Bid Type"] == bid_type
        return self.bid_figure_df[mask]

    def _compute_agg_grouped_by_year_and_bid_type(
        self, agg_func: Callable, agg_column: str
    ) -> pd.DataFrame:
        df = self.bid_figure_df.copy()
        # Add year column
        df["Year"] = df["Letting Date"].dt.year

        # Remove extra columns
        filtered_df = df.filter(["Year", "Bid Type", agg_column])

        # Compute aggregation
        agg = filtered_df.groupby(by=["Year", "Bid Type"]).agg(agg_func)

        return agg

    def summary_table_df(self) -> pd.DataFrame:
        weighted_mean = lambda x: np.average(
            x, weights=self.bid_figure_df.loc[x.index, "Quantity"]
        )
        avg_unit_price = self._compute_agg_grouped_by_year_and_bid_type(
            weighted_mean, "Unit Price"
        )
        contract_occur_count = self._compute_agg_grouped_by_year_and_bid_type(
            np.count_nonzero, "contract_id"
        )
        total_quanity = self._compute_agg_grouped_by_year_and_bid_type(
            np.sum, "Quantity"
        )

        joined = avg_unit_price.join(
            other=[contract_occur_count, total_quanity], how="left"
        )

        df = joined.reset_index()
        out_df = pd.DataFrame()
        out_df["Year"] = df["Year"]
        out_df["Bid Type"] = df["Bid Type"]
        out_df["Average Unit Price"] = df["Unit Price"].apply(lambda x: f"${x:,.2f}")
        out_df["Total Quanity"] = df["Quantity"].apply(lambda x: f"{x:,.0f}")
        out_df["Count of Bids Aggregated"] = df["contract_id"]

        return out_df

    def box_plot_df(self) -> pd.DataFrame:
        df = self.bid_figure_df.copy()

        # Add year column
        df["Year"] = df["Letting Date"].dt.year
        # Remove extra columns
        filtered_df = df.filter(["Year", "Bid Type", "Unit Price"])

        return filtered_df
