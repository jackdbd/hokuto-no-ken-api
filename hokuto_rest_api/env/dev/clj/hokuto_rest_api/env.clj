(ns hokuto-rest-api.env
  (:require
   [selmer.parser :as parser]
   [clojure.tools.logging :as log]
   [hokuto-rest-api.dev-middleware :refer [wrap-dev]]))

(def defaults
  {:init
   (fn []
     (parser/cache-off!)
     (log/info "\n-=[hokuto_rest_api started successfully using the development profile]=-"))
   :stop
   (fn []
     (log/info "\n-=[hokuto_rest_api has shut down successfully]=-"))
   :middleware wrap-dev})
