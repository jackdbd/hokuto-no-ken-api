-- :name get-users
-- :command :query
-- :result :raw
-- :doc Get all user records from the `users` table
SELECT * FROM users;

-- :name get-paginated-users
-- :command :query
-- :result :raw
-- :doc Get a subset of users
-- This uses [raw SQL parameters](https://www.hugsql.org/#param-sql)
SELECT * FROM users
LIMIT :sql:limit
OFFSET :sql:offset;

-- :name get-total-users
-- :command :query
-- :result :raw
-- :doc Get the number of all records in the `users` table
SELECT
    count(*) as total
FROM
    users;

-- :name get-admins
-- :command :query
-- :result :raw
-- :doc Get all records from the `admins` view
SELECT * FROM admins;

-- :name get-user
-- :command :query
-- :result :one
-- :doc Retrieve a record from the `users` table, given the id.
SELECT
    *
FROM
    users
WHERE
    id = :id;

-- :name create-user!
-- :command :execute
-- :result :affected
-- :doc Create a new user record
INSERT
INTO
    users
    (first_name, last_name, email, pass)
VALUES
    (:first_name, :last_name, :email, :pass);

-- :name update-user-email!
-- :command :execute
-- :result :affected
-- :doc Update the email of an existing user
UPDATE
    users
SET
    email = :email
WHERE
    id = :id;

-- :name delete-user!
-- :command :execute
-- :result :affected
-- :doc Delete a user record given the id
DELETE
FROM
    users
WHERE
    id = :id;

-- :name seed-users!
-- :command :execute
-- :result :affected
-- :doc Seed the `users` table with some fakes.
-- This is a multi-record insert with [SQL Tuple Lists](https://www.hugsql.org/#param-tuple-list).
INSERT
INTO
    users
    (first_name, last_name, email, pass, is_admin, timestamp_registration, timestamp_last_login)
VALUES :t*:fake-users;
