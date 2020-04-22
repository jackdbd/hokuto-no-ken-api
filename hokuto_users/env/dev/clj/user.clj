(ns user
  "Userspace functions (useful in the REPL)."
  (:require [clojure.pprint :refer [pprint]]))

;; https://clojure.org/reference/repl_and_main#_tap
;; https://www.birkey.co/2018-10-26-datafy-and-tap%3E-in-clojure-1.10.html
(add-tap (bound-fn* pprint))

(defn start
  "Start the application.
  Start everything the application needs (i.e. HTTP server, environment, router,
  database, etc). Do NOT start the REPL server."
  []
  (prn "=== Start the app ==="))

(defn stop
  "Stop the application. Do NOT stop the REPL server."
  []
  (prn "=== Stop the app ==="))

(defn restart
  "Restart the application. Do NOT restart the REPL server."
  []
  (stop)
  (start))
