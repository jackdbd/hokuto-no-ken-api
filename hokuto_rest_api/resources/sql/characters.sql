-- :name get-characters
-- :command :query
-- :result :raw
-- :doc Get all character records from the characters table
SELECT * FROM characters;

-- :name get-paginated-characters
-- :command :query
-- :result :raw
-- :doc Get a subset of characters
-- This uses [raw SQL parameters](https://www.hugsql.org/#param-sql)
SELECT * FROM characters
LIMIT :sql:limit
OFFSET :sql:offset;

-- :name get-total-characters
-- :command :query
-- :result :raw
-- :doc Get the number of all records in the `characters` table
SELECT
    count(*) as total
FROM
    characters;

-- :name get-character-by-id
-- :command :query
-- :result :one
-- :doc Retrieve a character record given the id
SELECT
  *
FROM
    characters
WHERE
    id = :id;

-- :name create-character!
-- :command :execute
-- :result :affected
-- :doc Create a new character record
INSERT
INTO
    characters
    (id, name, name_kanji, name_romaji, avatar, url, first_appearance_anime, first_appearance_manga)
VALUES
    (:id, :name, :name_kanji, :name_romaji, :avatar, :url, :first_appearance_anime, :first_appearance_manga);

-- :name delete-character-by-id!
-- :command :execute
-- :result :affected
-- :doc Delete a character record given the id
DELETE
FROM
    characters
WHERE
    id = :id;

-- :name seed-characters!
-- :command :execute
-- :result :affected
-- :doc Seed the characters table with a few characters.
INSERT
INTO
    characters
    (id, name, name_kanji, name_romaji, avatar, url, first_appearance_anime, first_appearance_manga)
VALUES
    ('kenshiro-string-id', 'Kenshiro', 'ケンシロウ', 'Kenshirō', 'https://hokuto.fandom.com/wiki/Kenshiro?file=Kenshiro-profile.jpg', 'https://hokuto.fandom.com/wiki/Kenshiro', 1, 1),
    ('raoh-string-id', 'Raoh', 'ラオウ', 'Raō', 'https://hokuto.fandom.com/wiki/Raoh?file=Raoh_%28manga%29.jpg', 'https://hokuto.fandom.com/wiki/Raoh', 32, 42);
