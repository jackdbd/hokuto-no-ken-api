(ns hokuto-users.interceptor.user
  "Namespace for interceptors that deal with the `user` resource."
  (:require [hokuto-users.http-response :refer [created ok]]
            [io.pedestal.http.route :as route]))

(defn- enter-create-user
  "Create a user and add it to the `context` map, in the `tx-data` key. Then
  change the status code of the HTTP response and provide the URL of the newly
  created resource."
  [context]
  (def params (get-in context [:request :json-params]))

  (def db-id (str (gensym "l")))
  ; Don't add the user right away, add a function that will be invoked by the
  ; database interceptor.
  ; In order to provide the Location url we can call Pedestal route/url-for with
  ; the name of the route. Remember that by default in Pedestal the name of the
  ; route is the name of the last interceptor for that route.
  ; TODO: probably there is a cleaner way to build the Location URL.
  (def url (format "%s/%s" (route/url-for ::create-user) db-id))

  (def new-user
    {:age (:age params)
     :name (:name params)})

  (assoc context
         :response (created new-user "Location" url)
         :tx-data [assoc db-id new-user]))

(def create-user
  "An interceptor which creates a new user and add it to the `context` map."
  {:name ::create-user
   :enter enter-create-user})

(defn- enter-list-users
  "Update the HTTP response with a HTTP 200 status code (Ok) and the list of
  users."
  [{:keys [request] :as context}]
  (def users (get-in context [:request :database]))
  ; (prn "===> enter-list-users" users)
  (assoc context :response (ok users)))

(def list-users
  "An interceptor which reads the list of users from the `context` map."
  {:name ::list-users
   :enter enter-list-users})

(defn- enter-get-user
  "TODO: add docs."
  [context]
  (def user-id (get-in context [:request :path-params :user-id]))
  (if-let [user (get-in context [:request :database user-id])]
    (assoc context :response (ok user))
    context))

(def get-user
  "TODO: add docs."
  {:name ::get-user
   :enter enter-get-user})
