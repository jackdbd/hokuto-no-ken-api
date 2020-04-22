(ns hokuto-users.interceptor.database
  "Namespace for interceptors that deal with the database."
  (:require [hokuto-users.db :refer [database db-seed db-reset]]))

(defn- enter-db
  "Add a database connection to the `context` map."
  [context]
  ; Just for testing, we populate the database every time.
  ; (db-seed)
  ; (db-reset)
  (def context-with-db-connection (update context :request assoc :database @database))
  ; (prn "===> enter-db" (get-in context-with-db-connection [:request :database]))
  context-with-db-connection)

(defn- leave-db
  "Extract an operation and a collection of arguments from the `tx-data` key in
  the `context` map and perform a database call with those arguments. Then
  update the `context` map for the next interceptors."
  [context]
  ; If tx-data is available, perform db operation. Otherwise just return context
  (if-let [[op & args] (:tx-data context)]
    (do (apply swap! database op args)
        (assoc-in context [:request :database] @database)
        ; (prn "<=== leave-db tx-data" (get-in context [:request :database]))
        context)
    context))

(def database-interceptor
  "Connect to a database and get/modify data in it."
  {:name ::database-interceptor
   :enter enter-db
   :leave leave-db})
