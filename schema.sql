CREATE TABLE IF NOT EXISTS Inventory (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    publication_date DATE NOT NULL,
    isbn TEXT UNIQUE NOT NULL
);
