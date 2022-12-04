from dataclasses import dataclass

from .item_loader import (
    ItemResponseDF,
    ItemTableDF,
    load_item_data,
    transform_item_response_df,
)


@dataclass
class ItemData:
    item_response_df: ItemResponseDF = load_item_data()

    def get_item_table_data(self, spec_year: str) -> dict[str, str | int]:
        filtered_df = transform_item_response_df(self.item_response_df, spec_year)
        return filtered_df.to_dict(orient="records")

    def get_item_dict(self, id: int) -> dict[str, str | int]:
        filter = self.item_response_df["id"] == id
        single_item_df = self.item_response_df[filter]
        return single_item_df.to_dict(orient="records")[0]
