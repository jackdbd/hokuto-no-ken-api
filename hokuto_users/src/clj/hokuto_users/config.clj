(ns hokuto-users.config
  (:require
   [cprop.core :refer [load-config]]
   [cprop.source :as source]
   [mount.core :refer [args defstate]]))

(defstate env
  "Stateful component that holds all configuration properties of an environment.
  Many other stateful components will depend from this one (e.g. http-server,
  repl-server, *db*)."
  :start (load-config
          :merge [(args)
                  (source/from-system-props)
                  (source/from-env)]))
