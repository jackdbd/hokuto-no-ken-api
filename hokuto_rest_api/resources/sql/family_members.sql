-- :name seed-family-members!
-- :command :execute
-- :result :affected
-- :doc Seed the `family_members` table with some records.
INSERT
INTO
    family_members
    (relative_left_id, relative_right_id)
VALUES
    ('kenshiro-string-id', 'raoh-string-id');
