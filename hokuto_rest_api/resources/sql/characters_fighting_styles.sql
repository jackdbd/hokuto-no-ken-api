-- :name seed-characters-fighting-styles!
-- :command :execute
-- :result :affected
-- :doc Seed the `characters_fighting_styles` table with some records.
INSERT
INTO
    characters_fighting_styles
    (character_id, fighting_style_id)
VALUES
    ('kenshiro-string-id', 'hokuto-string-id');
