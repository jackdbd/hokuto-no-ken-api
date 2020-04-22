# hokuto_users

TODO

## Build

```sh
lein uberjar
java -jar target/uberjar/hokuto_users.jar
```

## Development

This project uses [Leiningen 2.0](https://github.com/technomancy/leiningen).

Code formatting with [cljfmt](https://github.com/weavejester/cljfmt)

```sh
lein cljfmt check
lein cljfmt fix
```

Create a new database migration with [luminus-migrations](https://github.com/luminus-framework/luminus-migrations), then apply all `up` migrations.

```sh
# From the REPL
(db-create-migration "add-<table-name>-table")
(db-migrate)
```

## Tests

This project uses [lein-test-refresh](https://github.com/jakemcc/lein-test-refresh). Run `lein test-refresh` and write tests while developing.
