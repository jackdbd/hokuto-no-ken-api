-- :doc Create `characters_categories` associative table.
CREATE TABLE characters_categories (
    character_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    FOREIGN KEY(character_id) REFERENCES characters(id),
    FOREIGN KEY(category_id) REFERENCES categories(id),
    -- The primary key of this table is a table-constraint.
    -- https://sqlite.org/syntax/table-constraint.html
    PRIMARY KEY (character_id, category_id)
);
