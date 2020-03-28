-- :name get-voice-actors
-- :command :query
-- :result :raw
-- :doc Get all records from the `voice_actors` table
SELECT * FROM voice_actors;

-- :name seed-voice-actors!
-- :command :execute
-- :result :affected
-- :doc Seed the `voice_actors` table with some records.
INSERT
INTO
    voice_actors
    (id, name, url)
VALUES
    ('akira-kamiya-string-id', 'Akira Kamiya', 'https://hokuto.fandom.com/wiki/Akira_Kamiya'),
    ('takehito-koyasu-string-id', 'Takehito Koyasu', 'https://hokuto.fandom.com/wiki/Takehito_Koyasu');
