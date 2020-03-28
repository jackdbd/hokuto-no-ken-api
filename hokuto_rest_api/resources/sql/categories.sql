-- :name get-categories
-- :command :query
-- :result :raw
-- :doc Get all category records from the categories table
SELECT * FROM categories;

-- :name seed-categories!
-- :command :execute
-- :result :affected
-- :doc Seed the categories table with a few categories.
INSERT
INTO
    categories
    (id, name, url)
VALUES
    ('killed-by-kenshiro-string-id', 'Characters killed by Kenshirō', 'https://hokuto.fandom.com/wiki/Category:Characters_killed_by_Kenshir%C5%8D'),
    ('minions-of-raoh-string-id', 'Minions of Raoh', 'https://hokuto.fandom.com/wiki/Category:Minions_of_Raoh');
