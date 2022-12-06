from .item_loader import get_item_table_df, load_transformed_item_df

ItemDict = dict[str, str | int]
ItemTableData = list[ItemDict]


class ItemData:
    def __init__(self) -> None:
        self._transformed_item_df = load_transformed_item_df()

    def get_item_dict(self, id: int) -> ItemDict:
        filter = self._transformed_item_df["id"] == id
        single_item_df = self._transformed_item_df[filter]
        return single_item_df.to_dict(orient="records")[0]

    def query(self, spec_year: str, search_value: str) -> ItemTableData:
        if search_value is None:
            return []

        value = search_value.strip().upper()

        item_number_expr = "`Item Number`.str.contains(@value)"
        short_desc_expr = "`Short Description`.str.contains(@value)"
        long_desc_expr = "`Long Description`.str.contains(@value)"
        full_expr = f"{item_number_expr} or {short_desc_expr} or {long_desc_expr}"

        df = get_item_table_df(self._transformed_item_df, spec_year)
        filtered_df = df.query(expr=full_expr, inplace=False)

        return filtered_df.to_dict(orient="records")
