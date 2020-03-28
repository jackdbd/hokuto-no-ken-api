# Hokuto REST API

## Development

This project uses [Leiningen 2.0](https://github.com/technomancy/leiningen).

Code formatting with [cljfmt](https://github.com/weavejester/cljfmt)

```sh
# From the command line
lein cljfmt fix
```

Create a new database migration with [luminus-migrations](https://github.com/luminus-framework/luminus-migrations), then apply all `up` migrations.

```sh
# From the REPL
(db-create-migration "add-<table-name>-table")
(db-migrate)
```
