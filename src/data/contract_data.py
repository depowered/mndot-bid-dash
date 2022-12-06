from .contract_loader import (
    ContractDateDF,
    ContractResponseDF,
    get_contract_date_df,
    load_contract_response_df,
)


class ContractData:
    def __init__(self) -> None:
        self._contract_response_df: ContractResponseDF = load_contract_response_df()
        self.contract_date_df: ContractDateDF = get_contract_date_df(
            self._contract_response_df
        )
