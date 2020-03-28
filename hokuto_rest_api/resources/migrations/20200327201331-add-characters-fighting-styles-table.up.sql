-- :doc Create `characters_fighting_styles` table.
CREATE TABLE characters_fighting_styles (
    character_id TEXT NOT NULL,
    fighting_style_id TEXT NOT NULL,
    FOREIGN KEY(character_id) REFERENCES characters(id),
    FOREIGN KEY(fighting_style_id) REFERENCES fighting_styles(id),
    PRIMARY KEY (character_id, fighting_style_id)
);
