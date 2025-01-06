from sqlite3 import Connection
from typing import Optional

from stock_picks_optimizer.core.domain.models import StockGroup


class AddStockGroupUseCase:
    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn

    def invoke(self, stock_group: StockGroup) -> Optional[int]:
        curr = self.__db_conn.cursor()
        curr.execute(
            "INSERT INTO stock_group(name,budget) VALUES(?,?)",
            (stock_group.name, stock_group.budget),
        )
        self.__db_conn.commit()

        stock_group_id = curr.lastrowid
        for pick in stock_group.picks:
            curr.execute(
                "INSERT INTO stock_pick(symbol,percentage,stock_group_id) VALUES(?,?,?)",
                (pick.symbol, pick.percentage, stock_group_id),
            )
        self.__db_conn.commit()

        return stock_group_id
