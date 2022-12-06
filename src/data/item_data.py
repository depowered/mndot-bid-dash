from .item_loader import (
    ItemResponseDF,
    ItemTableDF,
    load_item_response_df,
    transform_item_response_df,
)

ItemDict = dict[str, str | int]
ItemTableData = list[ItemDict]


class ItemData:
    def __init__(self) -> None:
        self._item_response_df: ItemResponseDF = load_item_response_df()
        self._2016_item_table_df: ItemTableDF = transform_item_response_df(
            self._item_response_df, "2016"
        )
        self._2018_item_table_df: ItemTableDF = transform_item_response_df(
            self._item_response_df, "2018"
        )
        self._2020_item_table_df: ItemTableDF = transform_item_response_df(
            self._item_response_df, "2020"
        )

    def _get_item_table_df(self, spec_year: str) -> ItemTableDF:
        if spec_year == "2016":
            return self._2016_item_table_df
        elif spec_year == "2018":
            return self._2018_item_table_df
        else:
            return self._2020_item_table_df

    def get_item_dict(self, id: int) -> ItemDict:
        filter = self._item_response_df["id"] == id
        single_item_df = self._item_response_df[filter]
        return single_item_df.to_dict(orient="records")[0]

    def query(self, spec_year: str, search_value: str) -> ItemTableData:
        if search_value is None:
            return []

        value = search_value.strip().upper()

        item_number_expr = "`Item Number`.str.contains(@value)"
        short_desc_expr = "`Short Description`.str.contains(@value)"
        long_desc_expr = "`Long Description`.str.contains(@value)"
        full_expr = f"{item_number_expr} or {short_desc_expr} or {long_desc_expr}"

        df = self._get_item_table_df(spec_year)
        filtered_df = df.query(expr=full_expr, inplace=False)

        return filtered_df.to_dict(orient="records")
