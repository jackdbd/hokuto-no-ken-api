-- :doc Create `allegiances` table.
CREATE TABLE allegiances (
    ally_left_id TEXT NOT NULL,
    ally_right_id TEXT NOT NULL,
    -- SQL foreign key constraints to enforce the relationship between records
    -- in this table and records in the `characters` table.
    FOREIGN KEY(ally_left_id) REFERENCES characters(id),
    FOREIGN KEY(ally_right_id) REFERENCES characters(id),
    -- The primary key of this table is a table-constraint.
    -- https://sqlite.org/syntax/table-constraint.html
    PRIMARY KEY (ally_left_id, ally_right_id)
);
