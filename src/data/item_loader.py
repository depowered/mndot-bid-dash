import json

import pandas as pd
import pandera as pa
import requests
from pandera.typing import Series

from . import API_SERVER_URL


#
# Fetch data from server and create initial dataframe
#
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


#
# Preprocess initial data frame
#
class TransformedItemDF(pa.SchemaModel):
    id: Series[int]
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit: Series[str] = pa.Field(alias="Unit Name")
    unit_abbreviation: Series[str] = pa.Field(alias="Plan Unit Description")
    in_spec_2016: Series[pa.Bool]
    in_spec_2018: Series[pa.Bool]
    in_spec_2020: Series[pa.Bool]
    in_spec_2022: Series[pa.Bool]


def transform_item_response_df(item_response_df: ItemResponseDF) -> TransformedItemDF:
    df = pd.DataFrame()
    df["id"] = item_response_df["id"]
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
    df["in_spec_2016"] = item_response_df["in_spec_2016"]
    df["in_spec_2018"] = item_response_df["in_spec_2018"]
    df["in_spec_2020"] = item_response_df["in_spec_2020"]
    df["in_spec_2022"] = item_response_df["in_spec_2022"]

    return TransformedItemDF(df)


def load_transformed_item_df() -> TransformedItemDF:
    json_str = _fetch_all_item_data()
    item_response_df = _read_item_json(json_str)
    transformed_item_df = transform_item_response_df(item_response_df)

    return transformed_item_df


#
# Prepare for display in app
#
class ItemTableDF(pa.SchemaModel):
    id: Series[int]
    item_number: Series[str] = pa.Field(alias="Item Number")
    short_description: Series[str] = pa.Field(alias="Short Description")
    long_description: Series[str] = pa.Field(alias="Long Description")
    unit: Series[str] = pa.Field(alias="Unit Name")
    unit_abbreviation: Series[str] = pa.Field(alias="Plan Unit Description")
    spec_year: Series[str] = pa.Field(alias="Spec Year")

    class Config:
        strict = "filter"  # Drop all columns not defined in schema


def get_item_table_df(
    transformed_item_df: TransformedItemDF, spec_year: str
) -> ItemTableDF:
    filter = transformed_item_df[f"in_spec_{spec_year}"]
    filtered_df = transformed_item_df[filter].copy()
    filtered_df["Spec Year"] = spec_year

    return ItemTableDF(filtered_df)
