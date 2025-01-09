from sqlite3 import Connection
from typing import List

from stock_picks_optimizer.core.domain.models import StockGroup, StockPick
from stock_picks_optimizer.core.use_cases import FetchStockGroupByNameUseCase


class AddStockGroupUseCase:
    def __init__(
        self,
        db_conn: Connection,
        fetch_stock_group_by_name_use_case: FetchStockGroupByNameUseCase,
    ):
        self.__db_conn = db_conn
        self.__fetch_stock_group_by_name_use_case = fetch_stock_group_by_name_use_case

    def invoke(self, name: str, budget: float, picks: List[StockPick]) -> StockGroup:
        curr = self.__db_conn.cursor()
        curr.execute(
            "INSERT INTO stock_group(name, budget) VALUES(?,?)",
            (name, budget),
        )
        self.__db_conn.commit()

        stock_group_id = curr.lastrowid
        for pick in picks:
            curr.execute(
                "INSERT INTO stock_pick(symbol, percentage, stock_group_id) VALUES(?,?,?)",
                (pick.symbol, pick.percentage, stock_group_id),
            )
        self.__db_conn.commit()

        result = self.__fetch_stock_group_by_name_use_case.invoke(name)
        if result is None:
            raise Exception("something went wrong")
        else:
            return result
