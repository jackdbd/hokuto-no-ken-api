(defproject hokuto_users "0.1.0-SNAPSHOT"
  :description "Users API with Pedestal"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  
  :dependencies [[cheshire "5.10.0"]
                 [clojure.java-time "0.3.2"]
                 [com.github.javafaker/javafaker "1.0.2"]
                 [conman "0.8.4"]
                 [cprop "0.1.16"]
                 [io.pedestal/pedestal.jetty "0.5.7"]
                 [io.pedestal/pedestal.service "0.5.7"]
                 [luminus-migrations "0.6.7"]
                 [mount "0.1.16"]
                 [nrepl "0.6.0"]
                 [org.clojure/clojure "1.10.0"]
                 [org.xerial/sqlite-jdbc "3.30.1"]]
  
  :min-lein-version "2.0.0"
  
  :source-paths ["src/clj"]
  :test-paths ["test/clj"]
  
  :resource-paths ["config" "resources"]
  :target-path "target/%s/"
  :main hokuto-users.server

  :plugins [[lein-cljfmt "0.6.7"]]
  :cljfmt {:indentation? true}
  
  :profiles {:uberjar {:omit-source true
                       :aot :all
                       :uberjar-name "hokuto_users.jar"
                       :source-paths ["env/prod/clj"]
                       :resource-paths ["env/prod/resources"]}
             :dev           [:project/dev :profiles/dev]
             :test          [:project/dev :project/test :profiles/test]

             :project/dev  {:jvm-opts ["-Dconf=dev-config.edn" ]
                            :dependencies [[pjstadig/humane-test-output "0.10.0"]
                                           [prone "2020-01-17"]
                                           [ring/ring-devel "1.8.0"]
                                           [ring/ring-mock "0.4.0"]]
                            :plugins      [[com.jakemccrary/lein-test-refresh "0.24.1"]
                                           [jonase/eastwood "0.3.5"]] 
                            
                            :source-paths ["env/dev/clj" ]
                            :resource-paths ["env/dev/resources"]
                            :repl-options {:init-ns user
                                           :timeout 120000}
                            :injections [(require 'pjstadig.humane-test-output)
                                         (pjstadig.humane-test-output/activate!)]}
             :project/test {:jvm-opts ["-Dconf=test-config.edn" ]
                            :resource-paths ["env/test/resources"] }
             :profiles/dev {:aliases {"run-dev" ["trampoline" "run" "-m" "hokuto-users.server/run-dev"]}
                            :dependencies [[io.pedestal/pedestal.service-tools "0.5.7"]]
                            :plugins [[com.jakemccrary/lein-test-refresh "0.24.1"]]}
             :profiles/test {}})
