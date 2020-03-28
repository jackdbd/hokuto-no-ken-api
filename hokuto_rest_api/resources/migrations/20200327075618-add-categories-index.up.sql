-- :doc Create secondary index based on the `name` column of the `categories`
-- table. The primary index is the implicit index created for the primary key
-- constraint.
-- https://sqlite.org/lang_createindex.html
-- An index should be created on the child key columns of each foreign key
-- constraint. The child key index does not have to be (and usually will not be)
-- a UNIQUE index.
-- https://sqlite.org/foreignkeys.html#fk_schemacommands
CREATE INDEX ix_categories_name ON categories(name);
