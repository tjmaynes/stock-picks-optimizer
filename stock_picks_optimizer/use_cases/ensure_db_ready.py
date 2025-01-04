from sqlite3 import Connection
from pathlib import Path


class EnsureDbReadyUseCase:
    def __init__(self, db_conn: Connection, migrations_dir_path: Path, db_path: Path):
        self.__db_conn = db_conn
        self.__migrations_dir_path = migrations_dir_path
        self.__db_path = db_path

    def invoke(self) -> None:
        if not Path(self.__db_path).exists():
            open(self.__db_path, "a").close()

        (current_version,) = next(
            self.__db_conn.cursor().execute("PRAGMA user_version"), (1,)
        )
        migrations = list(self.__migrations_dir_path.iterdir())

        for migration in migrations[current_version:]:
            cur = self.__db_conn.cursor()
            try:
                cur.executescript("begin;" + migration.read_text())
            except:
                cur.execute("rollback")
                raise
            else:
                cur.execute("commit")
