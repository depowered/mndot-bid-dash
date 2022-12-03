import json

import pandas as pd
import pandera as pa
from pandera.typing import Series
import requests


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


class ItemDataTableInput(pa.SchemaModel):
    id: Series[int] = pa.Field(alias="ID")
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit: Series[str] = pa.Field(alias="Unit Name")
    unit_abbreviation: Series[str] = pa.Field(alias="Plan Unit Description")
    spec_year: Series[str] = pa.Field(alias="Spec Year")


def _fetch_all_item_data_in_spec_year(api_server_url: str, spec_year: str) -> str:
    url = f"{api_server_url}/item/query/"
    params = {f"in_spec_{spec_year.strip()}": "true", "limit": 0}
    response = requests.get(url, params)
    decoded_json = response.json()

    return json.dumps(decoded_json["data"])


def _read_item_json(json_str: str) -> ItemResponseDF:
    df = pd.read_json(
        json_str, orient="records", dtype=ItemResponseDF.to_schema().dtypes
    )
    return ItemResponseDF(df)


def _transform_item_data(
    item_response_df: ItemResponseDF, spec_year: str
) -> ItemDataTableInput:
    df = pd.DataFrame()

    df["ID"] = item_response_df["id"]
    df["Item Number"] = (
        item_response_df["spec_code"]
        + "."
        + item_response_df["unit_code"]
        + "/"
        + item_response_df["item_code"]
    )
    df["Short Description"] = item_response_df["short_description"]
    df["Long Description"] = item_response_df["long_description"]
    df["Unit Name"] = item_response_df["unit"]
    df["Plan Unit Description"] = item_response_df["unit_abbreviation"]
    df["Spec Year"] = spec_year

    return ItemDataTableInput(df)


def load_all_items_in_spec_year(api_server_url: str, spec_year: str) -> ItemResponseDF:
    json_str = _fetch_all_item_data_in_spec_year(api_server_url, spec_year)
    item_response_df = _read_item_json(json_str)
    item_data_table_input = _transform_item_data(item_response_df, spec_year)

    return item_data_table_input
