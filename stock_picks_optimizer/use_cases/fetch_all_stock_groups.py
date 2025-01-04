from sqlite3 import Connection
from typing import List

from stock_picks_optimizer.domain.models import StockGroup, StockPick


class FetchAllStockGroupsUseCase:
    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn

    def invoke(self) -> List[StockGroup]:
        curr = self.__db_conn.cursor()

        stock_group_rows = curr.execute(
            "SELECT id, name, budget, is_active FROM stock_group"
        )

        results = []
        for raw_stock_group in stock_group_rows.fetchall():
            picks = []

            stock_pick_rows = curr.execute(
                "SELECT symbol, percentage, last_price FROM stock_pick WHERE stock_group_id=?",
                (raw_stock_group[0],),
            )

            for pick in stock_pick_rows.fetchall():
                picks.append(
                    StockPick(
                        symbol=pick[0],
                        percentage=pick[1],
                        last_price=pick[2],
                    )
                )

            results.append(
                StockGroup(
                    name=raw_stock_group[1],
                    budget=raw_stock_group[2],
                    is_active=bool(raw_stock_group[3]),
                    picks=picks,
                )
            )

        return results
