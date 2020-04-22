(ns hokuto-users.service
  (:require [hokuto-users.interceptor :refer [content-length-json-body-interceptor]]
            [hokuto-users.interceptor.database :refer [database-interceptor]]
            [hokuto-users.interceptor.debug-context :refer [debug-context-map]]
            [hokuto-users.interceptor.user :as intc-user]
            [io.pedestal.http :as http]
            [io.pedestal.http.body-params :as body-params]
            [io.pedestal.http.route :as route]
            [ring.util.response :as ring-resp]))

(def common-interceptors
  [
   ; Parse the body parameters sent along with the HTTP request (it supports
   ; several Content-Types, including JSON). This interceptor has only a :enter
   ; function.
   (body-params/body-params)
   ; Set Content-Type response header to application/json and coerce body to
   ; JSON. This interceptor has only a :leave function.
   http/json-body
   ; This interceptor manages the connection to database. It has both a :enter
   ; and a :leave function.
   database-interceptor])

(def custom-interceptors
  "Custom interceptors."
  [(body-params/body-params)
   content-length-json-body-interceptor])

(defn about-page
  [request]
  ;; When using `content-type-json-body` in the interceptor chain, response
  ;; bodies are just Clojure data that get turned into JSON strings.
  (ring-resp/response {:some-data 1
                       :msg (format "Clojure %s - served from %s"
                                    (clojure-version)
                                    (route/url-for ::about-page))}))

(defn home-page
  [request]
  ;; When using the `json-body` in the interceptor chain, response bodies are
  ;; just Clojure data that *stream* into the response OutputStream (as UTF-8).
  (if-let [name (get-in request [:query-params :name])]
    (ring-resp/response {:hello name})
    (ring-resp/response {:hello "world"})))

(defn update-user
  [request]
  (ring-resp/response {:updated-user "updated user here"}))

(defn delete-user
  [request]
  (ring-resp/response {:deleted-user "deleted user here"}))

(def routes
  "Definition of the routes for the HTTP service."
  #{["/" :get (conj common-interceptors `home-page)]
    ["/users" :get (conj common-interceptors intc-user/list-users)]
    ["/users" :post (conj common-interceptors intc-user/create-user)]
    ["/users/:user-id" :get (conj common-interceptors intc-user/get-user)]
    ["/users/:user-id" :put (conj common-interceptors update-user) :route-name :update-user]
    ["/users/:user-id" :delete (conj common-interceptors delete-user) :route-name :delete-user]
    ["/about" :get (conj custom-interceptors `about-page)]})

(def service-map
  "Configuration for a HTTP service."
  {:env :prod
   ::http/routes routes
   ::http/port 8080
   ::http/resource-path "/public"
   ::http/type :jetty
   ; Container options for Jetty http://pedestal.io/reference/jetty
   ::http/container-options {:h2? false
                             :h2c? true
                             :max-threads 50
                             :ssl? false}})
