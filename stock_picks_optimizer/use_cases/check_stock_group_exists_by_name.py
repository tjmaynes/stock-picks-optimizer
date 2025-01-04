from sqlite3 import Connection


class CheckStockGroupExistsByNameUseCase:
    def __init__(self, db_conn: Connection):
        self.__db_conn = db_conn

    def invoke(self, name: str) -> bool:
        curr = self.__db_conn.cursor()
        curr.execute("SELECT * FROM stock_group WHERE name=?", (name,))
        result = curr.fetchone()
        return result is not None
