-- :doc Create `family_members` table.
CREATE TABLE family_members (
    relative_left_id TEXT NOT NULL,
    relative_right_id TEXT NOT NULL,
    FOREIGN KEY(relative_left_id) REFERENCES characters(id),
    FOREIGN KEY(relative_right_id) REFERENCES characters(id),
    PRIMARY KEY (relative_left_id, relative_right_id)
);
