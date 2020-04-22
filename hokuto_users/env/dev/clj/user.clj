(ns user
  "Userspace functions (useful in the REPL)."
  (:require [clojure.pprint :refer [pprint]]
            [conman.core :as conman]
            [hokuto-users.config :refer [env]]
            [hokuto-users.db.core :as db]
            [hokuto-users.server :refer [repl-server]]
            [java-time :as jt]
            [luminus-migrations.core :as migrations]
            [mount.core :as mount])
  (:import (java.util UUID)))

;; https://clojure.org/reference/repl_and_main#_tap
;; https://www.birkey.co/2018-10-26-datafy-and-tap%3E-in-clojure-1.10.html
(add-tap (bound-fn* pprint))

(defn start
  "Start the application.
  Start everything the application needs (i.e. HTTP server, environment, router,
  database, etc). Do NOT start the REPL server."
  []
  (prn "=== Start the application ===")
  (mount/start-without #'repl-server))

(defn stop
  "Stop the application. Do NOT stop the REPL server."
  []
  (prn "=== Stop the application ===")
  (mount/stop-except #'repl-server))

(defn restart
  "Restart the application. Do NOT restart the REPL server."
  []
  (stop)
  (start))

(defn db-restart
  "Restart the database.

  Restarting the db means rebinding the SQL queries to Clojure functions and
  creating a new connection pool. It does not alter any data in the database.
  When we restart the database we use [conman](https://github.com/luminus-framework/conman)
  to rebind the SQL queries (it uses [hugSQL](https://www.hugsql.org/)) and to
  create a new connection pool (it uses [HikariCP](https://github.com/tomekw/hikari-cp))."
  []
  (mount/stop #'hokuto-users.db.core/*db*)
  (mount/start #'hokuto-users.db.core/*db*)
  (binding [*ns* 'hokuto-users.db.core]
    (conman/bind-connection
     hokuto-users.db.core/*db*
     "sql/user.sql")))

(defn db-reset
  "Reset the database (CAUTION: LOSS OF DATA).

  luminus-migrations is a small command line wrapper for Migratus. In Migratus
  resetting the database means applying all 'down' migrations, then applying all
  'up' migrations.

  [Migratus](https://github.com/yogthos/migratus)."
  []
  (println "Reset db: apply all 'down' migrations; then all 'up' migrations.")
  (migrations/migrate ["reset"] (select-keys env [:database-url])))

(defn db-migrate
  "Migrate the database up for all outstanding migrations (CAUTION: LOSS OF DATA).
  This applies all 'up' migrations that were not yet applied."
  []
  (println "Apply all 'up' db migrations.")
  (migrations/migrate ["migrate"] (select-keys env [:database-url])))

(defn db-rollback
  "Rollback latest database migration (CAUTION: LOSS OF DATA).
  This applies only the latest 'down' migration."
  []
  (println "Apply latest 'down' db migration.")
  (migrations/migrate ["rollback"] (select-keys env [:database-url])))

(defn db-create-migration
  "Create a new 'up' and 'down' migration file with a generated timestamp and
  `name`.
  You will need to edit those files and write the SQL statements (in the SQL
  dialect of your database of choice) to migrate the database yourself."
  [name]
  (migrations/create name (select-keys env [:database-url])))

(defn db-seed
  "Seed the database with some fakes (useful in the REPL).
  The fakes are generated with [java-faker](https://github.com/DiUS/java-faker)."
  []
  ;; https://github.com/DiUS/java-faker#usage-with-locales
  (def fakerIt (com.github.javafaker.Faker. (new java.util.Locale "it")))
  (def fakerJa (com.github.javafaker.Faker. (new java.util.Locale "ja")))
  (def fakerZh (com.github.javafaker.Faker. (new java.util.Locale "zh-CN")))

  (def now (jt/local-date-time))
  (def five-minutes-ago (jt/minus now (jt/minutes 5)))
  (def yesterday (jt/minus now (jt/days 1)))
  (def last-week (jt/minus now (jt/weeks 1)))

  (def fake-users [[(.toString (UUID/randomUUID))
                    (.firstName (.name fakerIt))
                    (.lastName (.name fakerIt))
                    (.emailAddress (.internet fakerIt))
                    (.password (.internet fakerIt))
                    (.past (.date fakerIt) 30, (java.util.concurrent.TimeUnit/DAYS))
                    five-minutes-ago]
                   [(.toString (UUID/randomUUID))
                    (.firstName (.name fakerJa))
                    (.lastName (.name fakerJa))
                    (.emailAddress (.internet fakerJa))
                    (.password (.internet fakerJa))
                    last-week
                    yesterday]
                   [(.toString (UUID/randomUUID))
                    (.firstName (.name fakerZh))
                    (.lastName (.name fakerZh))
                    (.emailAddress (.internet fakerZh))
                    (.password (.internet fakerZh))
                    last-week
                    nil]])

  (db/seed-user! {:fake-users fake-users}))
