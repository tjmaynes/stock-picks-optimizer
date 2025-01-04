from stock_picks_optimizer.domain.models import StockGroup
from stock_picks_optimizer.use_cases import (
    AddStockGroupUseCase,
    CheckStockGroupExistsByNameUseCase,
)


class AddDefaultStockGroupUseCase:
    def __init__(
        self,
        check_stock_group_exists_by_name_use_case: CheckStockGroupExistsByNameUseCase,
        add_stock_group_use_case: AddStockGroupUseCase,
    ):
        self.__check_stock_group_exists_by_name_use_case = (
            check_stock_group_exists_by_name_use_case
        )
        self.__add_stock_group_use_case = add_stock_group_use_case

    def invoke(self, stock_group: StockGroup) -> None:
        if not self.__check_stock_group_exists_by_name_use_case.invoke(
            stock_group.name
        ):
            self.__add_stock_group_use_case.invoke(stock_group)
