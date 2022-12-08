import json
from datetime import datetime

import pandas as pd
import pandera as pa
import requests
from pandera.typing import Series

from . import API_SERVER_URL
from .contract_data import ContractData
from .item_data import ItemData


class BidResponseDF(pa.SchemaModel):
    id: Series[int]
    contract_id: Series[int]
    bidder_id: Series[int]
    item_id: Series[int]
    quantity: Series[float]
    unit_price: Series[int]
    bid_type: Series[str]

    class Config:
        coerce = True


def _fetch_bid_data(item_id: int) -> str:
    url = f"{API_SERVER_URL}/bid/query/"
    params = {"limit": 0, "item_id": item_id}
    response = requests.get(url, params)
    decoded_json = response.json()

    return json.dumps(decoded_json["data"])


def _read_bid_json(json_str: str) -> BidResponseDF:
    df = pd.read_json(
        json_str, orient="records", dtype=BidResponseDF.to_schema().dtypes
    )
    return BidResponseDF(df)


class TransformedBidDF(pa.SchemaModel):
    bid_id: Series[int]
    contract_id: Series[int]
    bidder_id: Series[int]
    item_id: Series[int]
    quantity: Series[float] = pa.Field(alias="Quantity")
    unit_price: Series[int]
    unit_price_float: Series[float] = pa.Field(alias="Unit Price")
    bid_type: Series[str] = pa.Field(alias="Bid Type")


def _transform_bid_response_df(bid_response_df: BidResponseDF) -> TransformedBidDF:
    df = pd.DataFrame()
    df["bid_id"] = bid_response_df["id"]
    df["contract_id"] = bid_response_df["contract_id"]
    df["bidder_id"] = bid_response_df["bidder_id"]
    df["item_id"] = bid_response_df["item_id"]
    df["Quantity"] = bid_response_df["quantity"]
    df["unit_price"] = bid_response_df["unit_price"]
    df["Unit Price"] = bid_response_df["unit_price"].apply(lambda x: x / 100)
    df["Bid Type"] = bid_response_df["bid_type"].str.title()

    return TransformedBidDF(df)


class BidFigureDF(pa.SchemaModel):
    bid_id: Series[int]
    contract_id: Series[int]
    letting_date: Series[datetime] = pa.Field(alias="Letting Date")
    bidder_id: Series[int]
    item_id: Series[int]
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit: Series[str] = pa.Field(alias="Unit Name")
    unit_abbreviation: Series[str] = pa.Field(alias="Plan Unit Description")
    quantity: Series[float] = pa.Field(alias="Quantity")
    unit_price: Series[int]
    unit_price_float: Series[float] = pa.Field(alias="Unit Price")
    bid_type: Series[str] = pa.Field(alias="Bid Type")

    @classmethod
    def schema_column_names(cls) -> list[str]:
        return list(cls._collect_fields().keys())

    class Config:
        strict = "filter"


def _join_contract_and_item_data(
    transformed_bid_df: TransformedBidDF,
    item_data: ItemData,
    contract_data: ContractData,
) -> BidFigureDF:

    # Merge item data
    merge_items = transformed_bid_df.merge(
        item_data._transformed_item_df, how="left", left_on="item_id", right_on="id"
    )
    merge_contracts = merge_items.merge(
        contract_data.contract_date_df,
        how="left",
        on="contract_id",
    )

    # Drop extra columns by validating with output DF schema
    df_filtered = BidFigureDF(merge_contracts)

    # Arrange the columns in the order defined by BidFigureDF
    final_df = df_filtered[BidFigureDF.schema_column_names()]
    return final_df


def load_bid_figure_df(
    item_id: int, item_data: ItemData, contract_data: ContractData
) -> BidFigureDF:
    json_str = _fetch_bid_data(item_id)
    bid_response_df = _read_bid_json(json_str)
    transformed_bid_df = _transform_bid_response_df(bid_response_df)
    bid_figure_df = _join_contract_and_item_data(
        transformed_bid_df, item_data, contract_data
    )

    return bid_figure_df
