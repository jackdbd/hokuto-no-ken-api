-- :name get-allegiances
-- :command :query
-- :result :raw
-- :doc Get all records from the `allegiances` table.
SELECT * FROM allegiances;

-- :name seed-allegiances!
-- :command :execute
-- :result :affected
-- :doc Seed the `allegiances` table with some records.
INSERT
INTO
    allegiances
    (ally_left_id, ally_right_id)
VALUES
    ('kenshiro-string-id', 'raoh-string-id');
