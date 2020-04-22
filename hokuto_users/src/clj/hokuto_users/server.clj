(ns hokuto-users.server
  (:require [hokuto-users.service :as service]
            [io.pedestal.http :as http]
            [io.pedestal.http.route :as route]
            [io.pedestal.http.route.definition.table :refer [table-routes]])
  ; Tell the clojure compiler to generate a class for this namespace using the
  ; -main method as entry point.
  (:gen-class))

;; This is an adapted service map, that can be started and stopped.
;; From the REPL you can call http/start and http/stop on this service
(defonce runnable-service (http/create-server service/service-map))

(defn run-dev
  "The entry-point for 'lein run-dev'"
  [& args]
  (println "\nCreating your [DEV] server...")
  (-> service/service-map
      (merge {:env :dev
              ;; do not block thread that starts web server
              ::http/join? false
              ;; Routes can be a function that resolves routes. We can use this
              ;; to set the routes to be reloadable.
              ::http/routes #(route/expand-routes (deref #'service/routes))
              ;; All origins are allowed in dev mode
              ::http/allowed-origins {:creds true :allowed-origins (constantly true)}
              ;; Content Security Policy (CSP) is mostly turned off in dev mode
              ::http/secure-headers {:content-security-policy-settings {:object-src "'none'"}}})
      ;; Wire up interceptor chains
      http/default-interceptors
      http/dev-interceptors
      http/create-server
      http/start))

(defn print-routes
  "Print our application's routes"
  []
  (route/print-routes (table-routes service/routes)))

(defn named-route
  "Finds a route by name"
  [route-name]
  (->> service/routes
       table-routes
       (filter #(= route-name (:route-name %)))
       first))

(defn -main
  "The entry-point for 'lein run'"
  [& args]
  (println "\nCreating your server...")
  (http/start runnable-service))
