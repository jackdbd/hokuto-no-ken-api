-- :name get-fighting-styles
-- :command :query
-- :result :raw
-- :doc Get all records from the `fighting_styles` table
SELECT * FROM fighting_styles;

-- :name get-paginated-fighting-styles
-- :command :query
-- :result :raw
-- :doc Get a subset of fighting-styles
-- This uses [raw SQL parameters](https://www.hugsql.org/#param-sql)
SELECT * FROM fighting_styles
LIMIT :sql:limit
OFFSET :sql:offset;

-- :name get-fighting-styles-from-school
-- :command :query
-- :result :raw
-- :doc Get a subset of fighting-styles
SELECT * FROM fighting_styles
WHERE instr(lower(name), :school) > 0;

-- :name get-total-fighting-styles
-- :command :query
-- :result :raw
-- :doc Get the number of all records in the `fighting_styles` table
SELECT
    count(*) as total
FROM
    fighting_styles;

-- :name seed-fighting-styles!
-- :command :execute
-- :result :affected
-- :doc Seed the `fighting_styles` table with some records.
INSERT
INTO
    fighting_styles
    (id, name, url)
VALUES
    ('hokuto-string-id', 'Hokuto Shinken', 'https://hokuto.fandom.com/wiki/Hokuto_Shinken'),
    ('nanto-string-id', 'Nanto Seiken', 'https://hokuto.fandom.com/wiki/Nanto_Seiken');
