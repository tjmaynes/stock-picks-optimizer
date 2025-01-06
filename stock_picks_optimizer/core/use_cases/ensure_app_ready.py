from stock_picks_optimizer.core.domain.models import StockGroup, StockPick
from stock_picks_optimizer.core.use_cases import (
    AddDefaultStockGroupUseCase,
    EnsureDbReadyUseCase,
)


class EnsureAppReadyUseCase:
    def __init__(
        self,
        ensure_db_ready_use_case: EnsureDbReadyUseCase,
        add_default_stock_group_use_case: AddDefaultStockGroupUseCase,
    ):
        self.__ensure_db_ready_use_case = ensure_db_ready_use_case
        self.__add_default_stock_group_use_case = add_default_stock_group_use_case

    def invoke(self) -> None:
        self.__ensure_db_ready_use_case.invoke()

        self.__add_default_stock_group_use_case.invoke(
            StockGroup(
                name="Default",
                budget=2000.0,
                picks=[
                    StockPick(symbol="VTI", percentage=0.6),
                    StockPick(symbol="VXUS", percentage=0.3),
                    StockPick(symbol="BND", percentage=0.1),
                ],
            )
        )
