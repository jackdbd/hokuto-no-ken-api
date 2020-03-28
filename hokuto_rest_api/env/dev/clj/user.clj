(ns user
  "Userspace functions (useful in the REPL)."
  (:require
   [clojure.pprint :refer [pprint]]
   [clojure.spec.alpha :as s]
   [conman.core :as conman]
   [expound.alpha :as expound]
   [hokuto-rest-api.config :refer [env]]
   [hokuto-rest-api.core :refer [repl-server]]
   [hokuto-rest-api.db.core :as db]
   [hokuto-rest-api.routes.services :as api]
   [java-time :as jt]
   [luminus-migrations.core :as migrations]
   [mount.core :as mount]))

;; monkey-patch spec errors to make them more human-friendly
;; https://github.com/bhb/expound/blob/master/doc/faq.md
(alter-var-root #'s/*explain-out* (constantly expound/printer))

;; https://clojure.org/reference/repl_and_main#_tap
;; https://www.birkey.co/2018-10-26-datafy-and-tap%3E-in-clojure-1.10.html
(add-tap (bound-fn* pprint))

(defn start
  "Start the application.
  Start everything the application needs (i.e. HTTP server, environment, router,
  database, etc). Do NOT start the REPL server."
  []
  (mount/start-without #'repl-server))

(defn stop
  "Stop the application. Do NOT stop the REPL server."
  []
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
  (mount/stop #'hokuto-rest-api.db.core/*db*)
  (mount/start #'hokuto-rest-api.db.core/*db*)
  (binding [*ns* 'hokuto-rest-api.db.core]
    (conman/bind-connection
     hokuto-rest-api.db.core/*db*
     "sql/allegiances.sql"
     "sql/categories.sql"
     "sql/characters.sql"
     "sql/characters_categories.sql"
     "sql/characters_fighting_styles.sql"
     "sql/characters_voice_actors.sql"
     "sql/family_members.sql"
     "sql/fighting_styles.sql"
     "sql/stats.sql"
     "sql/users.sql"
     "sql/voice_actors.sql")))

(defn ns-reload
  "Reload the user namespace.
  [Reload Clojure file in REPL](https://stackoverflow.com/questions/7658981/how-to-reload-a-clojure-file-in-repl)"
  []
  (use 'user :reload)
  ; (use '[clojure.tools.namespace.repl :only (refresh)])
  ; (refresh)
  ; (require 'user :reload-all)
  (println "Namespace user reloaded."))

(defn db-reset
  "Reset the database (CAUTION: LOSS OF DATA).
  luminus-migrations is a small command line wrapper for [Migratus](https://github.com/yogthos/migratus).
  In Migratus resetting the database means applying all 'down' migrations, then
  applying all 'up' migrations."
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

  (def fake-users [[(.firstName (.name fakerIt))
                    (.lastName (.name fakerIt))
                    (.emailAddress (.internet fakerIt))
                    (.password (.internet fakerIt))
                    1
                    (.past (.date fakerIt) 30, (java.util.concurrent.TimeUnit/DAYS))
                    five-minutes-ago]
                   [(.firstName (.name fakerJa))
                    (.lastName (.name fakerJa))
                    (.emailAddress (.internet fakerJa))
                    (.password (.internet fakerJa))
                    0
                    last-week
                    yesterday]
                   [(.firstName (.name fakerZh))
                    (.lastName (.name fakerZh))
                    (.emailAddress (.internet fakerZh))
                    (.password (.internet fakerZh))
                    1
                    last-week
                    nil]])

  ; (db/seed-categories!)
  ; (db/seed-characters!)
  ; (db/seed-fighting-styles!)
  (db/seed-users! {:fake-users fake-users})
  ; (db/seed-voice-actors!)

  ;; Some tables have foreign key constraints that reference the `characters`
  ;; table, the `categories` table, the `fighting_styles` table.
  ;; So we must populate those tables first.
  ; (db/seed-allegiances!)
  ; (db/seed-family-members!)
  ; (db/seed-characters-categories!)
  ; (db/seed-characters-fighting-styles!)
  ; (db/seed-characters-voice-actors!)
  )

(defn db-get-first-four-users
  []
  (db/get-paginated-users {:limit 4 :offset 0}))

(defn db-get-first-four-characters
  []
  (db/get-paginated-characters {:limit 4 :offset 0}))

(defn db-get-first-four-fighting-styles
  []
  (db/get-paginated-fighting-styles {:limit 4 :offset 0}))

(defn api-characters-get
  "Invoke the `characters-get` handler directly, with no middlewares."
  []
  (api/characters-get {:server-name "my-server"
                       :server-port "3000"
                       :uri "/my-api-endpoint"
                       :params {:page {:offset 0}}}))

(defn api-users-get
  "Invoke the `users-get` handler directly, with no middlewares."
  []
  (api/users-get {:server-name "my-server"
                  :server-port "3000"
                  :uri "/my-api-endpoint"
                  :params {:page {:offset 0}}}))

(defn api-fighting-styles-get
  "Invoke the `fighting-styles-get` handler directly, with no middlewares."
  []
  (api/fighting-styles-get {:server-name "my-server"
                            :server-port "3000"
                            :uri "/my-api-endpoint"
                            :params {:page {:offset 0}}}))

(defn db-get-hokuto
  []
  (db/get-fighting-styles-from-school {:school "hokuto"}))

(defn db-get-nanto
  []
  (db/get-fighting-styles-from-school {:school "nanto"}))

(defn db-change-email []
  (let [email (format "my-email%1$s@gmail.com" (rand-int 99))]
    (db/update-user-email! {:email email :id "1"})))

(defn api-users-patch-email [email]
  (api/users-patch {:server-name "my-server"
                    :server-port "3000"
                    :uri "/my-api-endpoint"
                    :parameters {:body {:email email
                                        :id "1"}}}))

(defn api-users-post
  "Invoke the `users-post` handler directly, with no middlewares."
  []
  (api/users-post {:server-name "my-server"
                   :server-port "3000"
                   :uri "/my-api-endpoint"
                   :parameters {:body {:email "fake.email@gmail.com"
                                       :first_name "Fake first name"
                                       :last_name "Fake last name"
                                       :pass "some-password"}}}))

(defn api-users-delete
  "Invoke the `users-delete` handler directly, with no middlewares."
  [id]
  (api/users-delete {:server-name "my-server"
                     :server-port "3000"
                     :uri "/my-api-endpoint"
                     :parameters {:body {:id id}}}))
