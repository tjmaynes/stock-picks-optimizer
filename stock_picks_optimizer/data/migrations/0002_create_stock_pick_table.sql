PRAGMA migration_version=2;

CREATE TABLE IF NOT EXISTS stock_pick (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    percentage FLOAT NOT NULL,
    last_price FLOAT NULL,
    stock_group_id INTEGER NOT NULL,
    FOREIGN KEY (stock_group_id) REFERENCES stock_group(id) ON DELETE CASCADE ON UPDATE CASCADE
);