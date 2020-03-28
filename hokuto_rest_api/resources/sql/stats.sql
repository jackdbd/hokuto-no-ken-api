-- :name get-password-lengths
-- :command :query
-- :result :raw
-- :doc Get the minimum, maximum, average length of the users' passwords.
SELECT
    min(password_length) AS shortest,
    max(password_length) AS longest,
    avg(password_length) AS average
FROM
    (SELECT
        length(u.pass) AS password_length
    FROM
        users AS u);
