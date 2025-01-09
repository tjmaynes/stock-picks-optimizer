from stock_picks_optimizer.core.domain.models import StockGroup
from stock_picks_optimizer.core.use_cases import (
    AddStockGroupUseCase,
    FetchStockGroupByNameUseCase,
)


class AddDefaultStockGroupUseCase:
    def __init__(
        self,
        fetch_stock_group_by_name_use_case: FetchStockGroupByNameUseCase,
        add_stock_group_use_case: AddStockGroupUseCase,
    ):
        self.__fetch_stock_group_by_name_use_case = fetch_stock_group_by_name_use_case
        self.__add_stock_group_use_case = add_stock_group_use_case

    def invoke(self, stock_group: StockGroup) -> None:
        if not self.__fetch_stock_group_by_name_use_case.invoke(stock_group.name):
            self.__add_stock_group_use_case.invoke(
                stock_group.name, stock_group.budget, stock_group.picks
            )
