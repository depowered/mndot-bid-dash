import json
from datetime import date

import pandas as pd
import pandera as pa
import requests
from pandera.typing import Series

from . import API_SERVER_URL


class ContractResponseDF(pa.SchemaModel):
    id: Series[int]
    letting_date: Series[date]
    sp_number: Series[str]
    district: Series[str]
    county: Series[str]
    description: Series[str]
    winning_bidder_id: Series[int]

    class Config:
        coerce = True


def _fetch_all_contract_data() -> str:
    url = f"{API_SERVER_URL}/contract/all"
    params = {"limit": 0}
    response = requests.get(url, params)
    decoded_json = response.json()

    return json.dumps(decoded_json["data"])


def _read_contract_json(json_str: str) -> ContractResponseDF:
    df = pd.read_json(
        json_str, orient="records", dtype=ContractResponseDF.to_schema().dtypes
    )
    return ContractResponseDF(df)


def load_contract_response_df() -> ContractResponseDF:
    json_str = _fetch_all_contract_data()
    contract_response_df = _read_contract_json(json_str)

    return contract_response_df


class ContractDateDF(pa.SchemaModel):
    contract_id: Series[int]
    letting_date: Series[date] = pa.Field(alias="Letting Date")


def get_contract_date_df(contract_response_df: ContractResponseDF) -> ContractDateDF:
    df = pd.DataFrame()
    df["contract_id"] = contract_response_df["id"]
    df["Letting Date"] = contract_response_df["letting_date"]

    return ContractDateDF(df)
