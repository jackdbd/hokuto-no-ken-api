-- :doc Create `users` table.
-- Remember that SQLite have a dynamic type system and each datatype is
-- converted into one of 5 SQLite affinities.
-- https://www.sqlite.org/datatype3.html
CREATE TABLE users (
    -- A PRIMARY KEY column only becomes an integer primary key if the declared
    -- type name is exactly INTEGER.
    -- https://sqlite.org/lang_createtable.html#rowid
    -- https://sqlite.org/autoinc.html#the_autoincrement_keyword
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT NOT NULL,
    pass TEXT NOT NULL,
    -- SQLite stores boolean values as integers 0 (false) and 1 (true).
    is_admin BOOLEAN DEFAULT 0,
    is_active BOOLEAN,
    timestamp_registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    timestamp_last_login TIMESTAMP
);
