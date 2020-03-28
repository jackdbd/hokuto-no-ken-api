-- :name seed-characters-categories!
-- :command :execute
-- :result :affected
-- :doc Seed the `characters_categories` table with some records.
INSERT
INTO
    characters_categories
    (character_id, category_id)
VALUES
    ('raoh-string-id', 'killed-by-kenshiro-string-id');
