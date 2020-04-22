-- :name get-users
-- :command :query
-- :result :raw
-- :doc Get all user records from the `user` table
SELECT * FROM user;

-- :name get-paginated-users
-- :command :query
-- :result :raw
-- :doc Get a subset of users
-- This uses [raw SQL parameters](https://www.hugsql.org/#param-sql)
SELECT * FROM user
LIMIT :sql:limit
OFFSET :sql:offset;

-- :name get-total-users
-- :command :query
-- :result :raw
-- :doc Get the number of all records in the `user` table
SELECT
    count(*) as total
FROM
    user;

-- :name seed-user!
-- :command :execute
-- :result :affected
-- :doc Seed the `user` table with some fakes.
-- This is a multi-record insert with [SQL Tuple Lists](https://www.hugsql.org/#param-tuple-list).
INSERT
INTO
    user
    (id, first_name, last_name, email, pass, timestamp_registration, timestamp_last_login)
VALUES :t*:fake-users;
