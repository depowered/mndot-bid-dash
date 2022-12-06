import json

import pandas as pd
import pandera as pa
import requests
from pandera.typing import Series

from . import API_SERVER_URL


class ItemResponseDF(pa.SchemaModel):
    id: Series[pa.Int]
    spec_code: Series[pa.String]
    unit_code: Series[pa.String]
    item_code: Series[pa.String]
    short_description: Series[pa.String]
    long_description: Series[pa.String]
    unit: Series[pa.String]
    unit_abbreviation: Series[pa.String]
    in_spec_2016: Series[pa.Bool]
    in_spec_2018: Series[pa.Bool]
    in_spec_2020: Series[pa.Bool]
    in_spec_2022: Series[pa.Bool]

    class Config:
        coerce = True


class ItemTableDF(pa.SchemaModel):
    id: Series[int]
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit: Series[str] = pa.Field(alias="Unit Name")
    unit_abbreviation: Series[str] = pa.Field(alias="Plan Unit Description")
    spec_year: Series[str] = pa.Field(alias="Spec Year")


def _fetch_all_item_data() -> str:
    url = f"{API_SERVER_URL}/item/all"
    params = {"limit": 0}
    response = requests.get(url, params)
    decoded_json = response.json()

    return json.dumps(decoded_json["data"])


def _read_item_json(json_str: str) -> ItemResponseDF:
    df = pd.read_json(
        json_str, orient="records", dtype=ItemResponseDF.to_schema().dtypes
    )
    return ItemResponseDF(df)


def load_item_response_df() -> ItemResponseDF:
    json_str = _fetch_all_item_data()
    item_response_df = _read_item_json(json_str)

    return item_response_df


def transform_item_response_df(
    item_response_df: ItemResponseDF, spec_year: str
) -> ItemTableDF:
    filtered_df = item_response_df[item_response_df[f"in_spec_{spec_year}"]]

    df = pd.DataFrame()
    df["id"] = filtered_df["id"]
    df["Item Number"] = (
        filtered_df["spec_code"]
        + "."
        + filtered_df["unit_code"]
        + "/"
        + filtered_df["item_code"]
    )
    df["Short Description"] = filtered_df["short_description"]
    df["Long Description"] = filtered_df["long_description"]
    df["Unit Name"] = filtered_df["unit"]
    df["Plan Unit Description"] = filtered_df["unit_abbreviation"]
    df["Spec Year"] = spec_year

    return ItemTableDF(df)
