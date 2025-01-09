from sqlite3 import Connection
from typing import Optional

from stock_picks_optimizer.core.domain.models import StockGroup


class FetchStockGroupByNameUseCase:
    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn

    def invoke(self, name: str) -> Optional[StockGroup]:
        curr = self.__db_conn.cursor()
        curr.execute("SELECT * FROM stock_group WHERE name=?", (name,))
        result = curr.fetchone()
        return (
            StockGroup(
                name=result[0], budget=result[1], picks=result[2], is_active=result[3]
            )
            if result is not None
            else None
        )
