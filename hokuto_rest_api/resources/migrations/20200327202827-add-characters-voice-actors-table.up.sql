-- :doc Create `characters_voice_actors` table.
CREATE TABLE characters_voice_actors (
    character_id TEXT NOT NULL,
    voice_actor_id TEXT NOT NULL,
    FOREIGN KEY(character_id) REFERENCES characters(id),
    FOREIGN KEY(voice_actor_id) REFERENCES voice_actors(id),
    PRIMARY KEY (character_id, voice_actor_id)
);
