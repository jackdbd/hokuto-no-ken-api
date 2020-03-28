-- doc: Create `characters` table.
CREATE TABLE characters (
    -- SQLite would allow NULL values in the PRIMARY KEY column (except when
    -- the column is an INTEGER). Since it does not make sense to have a NULL
    -- primary key, we enforce the string `id` to be NOT NULL.
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    name_kanji TEXT,
    name_romaji TEXT,
    avatar TEXT,
    url TEXT,
    first_appearance_anime INTEGER,
    first_appearance_manga INTEGER
);
