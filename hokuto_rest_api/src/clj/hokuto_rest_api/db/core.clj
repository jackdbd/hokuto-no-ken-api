(ns hokuto-rest-api.db.core
  "This namespace represents the bridge between the database world and the 
  clojure world. It manages the connection pool to the SQLite database and
  handles the conversion between objects coming from the SQL world into the
  Clojure world, and viceversa."
  (:require
   [clojure.java.jdbc :as jdbc]
   [conman.core :as conman]
   [java-time.pre-java8 :as jt]
   [hokuto-rest-api.config :refer [env]]
   [mount.core :refer [defstate]]))

;; The database credentials are stored in .edn files, which are NOT tracked in 
;; version control.
(defstate ^:dynamic *db*
  "Stateful component that holds the HikariCP connection pool.
  The connection to the database is managed by conman. The lifecycle of the
  connection pool is managed by [mount](https://github.com/tolitius/mount)."
  :start (conman/connect! {:jdbc-url (env :database-url)})
  :stop (conman/disconnect! *db*))

;; Bind all SQL commands to the connection pool (conman uses hugSQL).
(conman/bind-connection
 *db*
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
 "sql/voice_actors.sql")

;; Extend the `IResultSetReadColumn` protocol to transform values after reading
;; them from the database.
;; https://luminusweb.com/docs/database.html
;; https://clojure.github.io/java.jdbc/#clojure.java.jdbc/IResultSetReadColumn
(extend-protocol jdbc/IResultSetReadColumn
  ;; Convert `java.sql.Timestamp` objects to `java.time.LocalDateTime` objects.
  ;; https://docs.oracle.com/javase/8/docs/api/java/time/LocalDateTime.html
  java.sql.Timestamp
  (result-set-read-column [val rsmeta idx]
    (.toLocalDateTime val))
  ;; Convert `java.sql.Date` objects to `java.time.LocalDate` objects.
  ;; https://docs.oracle.com/javase/8/docs/api/java/time/LocalDate.html
  java.sql.Date
  (result-set-read-column [val rsmeta idx]
    (.toLocalDate val))
  ;; Convert `java.sql.Time `objects to `java.time.LocalTime` objects.
  ;; https://docs.oracle.com/javase/8/docs/api/java/time/LocalTime.html
  java.sql.Time
  (result-set-read-column [val rsmeta idx]
    (.toLocalTime val)))

;; Extend the `ISQLValue` protocol to convert a Clojure value into a SQL value.
;; https://clojure.github.io/java.jdbc/#clojure.java.jdbc/ISQLValue
;; https://github.com/dm3/clojure.java-time
(extend-protocol jdbc/ISQLValue
  java.util.Date
  (sql-value [val]
    (java.sql.Timestamp. (.getTime val)))
  java.time.LocalTime
  (sql-value [val]
    (jt/sql-time val))
  java.time.LocalDate
  (sql-value [val]
    (jt/sql-date val))
  java.time.LocalDateTime
  (sql-value [val]
    (jt/sql-timestamp val))
  java.time.ZonedDateTime
  (sql-value [val]
    (jt/sql-timestamp val)))
