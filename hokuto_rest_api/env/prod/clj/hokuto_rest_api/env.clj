(ns hokuto-rest-api.env
  (:require [clojure.tools.logging :as log]))

(def defaults
  {:init
   (fn []
     (log/info "\n-=[hokuto_rest_api started successfully]=-"))
   :stop
   (fn []
     (log/info "\n-=[hokuto_rest_api has shut down successfully]=-"))
   :middleware identity})
