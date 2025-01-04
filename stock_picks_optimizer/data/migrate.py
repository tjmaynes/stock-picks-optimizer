from sqlite3 import Connection
from pathlib import Path


def ensure_db_ready(
    db_conn: Connection, migrations_dir_path: Path, db_path: Path
) -> None:
    if not Path(db_path).exists():
        open(db_path, "a").close()

    (current_version,) = next(db_conn.cursor().execute("PRAGMA user_version"), (1,))
    migrations = list(migrations_dir_path.iterdir())

    for migration in migrations[current_version:]:
        cur = db_conn.cursor()
        try:
            cur.executescript("begin;" + migration.read_text())
        except:
            cur.execute("rollback")
            raise
        else:
            cur.execute("commit")
