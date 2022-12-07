from __future__ import annotations

from dataclasses import dataclass

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
