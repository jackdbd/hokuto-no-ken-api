-- :name seed-characters-voice-actors!
-- :command :execute
-- :result :affected
-- :doc Seed the `characters_voice_actors` table with some records.
INSERT
INTO
    characters_voice_actors
    (character_id, voice_actor_id)
VALUES
    ('kenshiro-string-id', 'akira-kamiya-string-id');
