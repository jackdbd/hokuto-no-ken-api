(ns hokuto-rest-api.routes.services
  "This namespace represents the REST service. It defines the API routes,
  enforces resource validation, handles content negotiation."
  (:require
   [clojure.java.io :as io]
   [clojure.java.jdbc :as jdbc]
   [clojure.tools.logging :as log]
   [hokuto-rest-api.db.core :as db]
   [hokuto-rest-api.middleware.exception :as exception]
   [hokuto-rest-api.middleware.formats :as formats]
   [reitit.coercion.spec :as spec-coercion]
   [reitit.ring.coercion :as coercion]
   [reitit.ring.middleware.multipart :as multipart]
   [reitit.ring.middleware.muuntaja :as muuntaja]
   [reitit.ring.middleware.parameters :as parameters]
   [reitit.swagger :as swagger]
   [reitit.swagger-ui :as swagger-ui]
   [ring.util.http-response :refer :all])
  (:import (java.util UUID)))

(def pagination {:default-page-offset 0 :results-per-page 4})

(defn characters-get
  "Handle a HTTP GET request and return some characters."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))

  (def offset (get-in request [:params :page :offset] (get pagination :default-page-offset)))
  (def limit (get-in pagination [:results-per-page]))
  (def total (int (get-in (first (db/get-total-characters db/*db*)) [:total])))
  (def last-page (int (Math/ceil (/ total limit))))

  (log/info "[characters-get] PARAMS" (get-in request [:params]))
  (def results-paginated (db/get-paginated-characters {:limit limit :offset offset}))
  (log/info "[characters-get] Retrieve" limit "of" total "characters")
  ;; (log/info "[select * from characters" (jdbc/query db/*db* ["select * from characters"]))

  (def body {:data {:characters results-paginated}
             :links {:last (format "http://%1$s:%2$s%3$s?page=%4$s" server-name server-port uri last-page)
                     :next (format "http://%1$s:%2$s%3$s?page[offset]=%4$s" server-name server-port uri offset)
                     :self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}})
  {:status 200 :body body})

(defn fighting-styles-get
  "Handle a HTTP GET request and return some fighting_styles."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))

  (def offset (get-in request [:params :page :offset] (get pagination :default-page-offset)))
  (def limit (get-in pagination [:results-per-page]))
  (def total (int (get-in (first (db/get-total-fighting-styles db/*db*)) [:total])))
  (def last-page (int (Math/ceil (/ total limit))))

  (log/info "[fighting-styles-get] PARAMS" (get-in request [:params]))
  (def results-paginated (db/get-paginated-fighting-styles {:limit limit :offset offset}))
  (log/info "[fighting-styles-get] Retrieve" limit "of" total "fighting styles")

  (def body {:data {:fighting_styles results-paginated}
             :links {:last (format "http://%1$s:%2$s%3$s?page=%4$s" server-name server-port uri last-page)
                     :next (format "http://%1$s:%2$s%3$s?page[offset]=%4$s" server-name server-port uri offset)
                     :self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}})
  {:status 200 :body body})

(defn user-get
  "Handle a HTTP GET request with path parameters and return a particular user."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))
  ;; (log/info "[user-delete] uri" uri)

  (def id (get-in request [:path-params :id]))

  (if-let [user (db/get-user {:id id})]
    (do
      (log/info "[user-get] user id =" id "FOUND")
      {:status 200
       :body {:data {:id id
                     :first_name (:first_name user)
                     :last_name (:last_name user)}
              :links {:all-users (format "http://%1$s:%2$s/api/users" server-name server-port)
                      :self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}}})
    (do
      (log/info "[user-get] user id =" id "NOT FOUND")
      {:status 404
       :body {:data {}
              :links {:all-users (format "http://%1$s:%2$s/api/users" server-name server-port)}}})))

(defn users-get
  "Handle a HTTP GET request and return some users."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))

  (def offset (get-in request [:params :page :offset] (get pagination :default-page-offset)))
  (def limit (get-in pagination [:results-per-page]))
  (def total (int (get-in (first (db/get-total-users db/*db*)) [:total])))
  (def last-page (int (Math/ceil (/ total limit))))

  (log/info "[users-get] PARAMS" (get-in request [:params]))
  (def results-paginated (db/get-paginated-users {:limit limit :offset offset}))
  (log/info "[users-get] Retrieve" limit "of" total "users")

  ;; (log/info "[users-get] URI" (get-in request [:uri]))
  ;; (log/info "[users-get] COOKIES" (get-in request [:cookies]))
  ;; (log/info "[users-get] HEADERS" (get-in request [:headers]))
  ;; (log/info "[users-get] BODY" (get-in request [:body]))
  (def users (if (= "1" (get-in request [:params :is-admin]))
               (db/get-admins db/*db*)
               results-paginated))
  (def body {:data {:users users}
             :links {:last (format "http://%1$s:%2$s%3$s?page=%4$s" server-name server-port uri last-page)
                     :next (format "http://%1$s:%2$s%3$s?page[offset]=%4$s" server-name server-port uri offset)
                     :self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}})
  {:status 200 :body body})

(defn users-post
  "Handle a HTTP POST request and return the id of the newly created user."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))

  (def req-body (:body (:parameters request)))
  (log/info "[users-post]" "body" req-body)

  (def id (.toString (UUID/randomUUID)))

  (db/create-user! {:id id
                    :first_name (:first_name req-body)
                    :last_name (:last_name req-body)
                    :email (:email req-body)
                    :pass (:pass req-body)})

  (def res-body {:data {:id id}
                 :links {:all-users (format "http://%1$s:%2$s%3$s" server-name server-port uri)
                         :this-user (format "http://%1$s:%2$s%3$s/%4$s" server-name server-port uri id)}})
  {:status 201 :body res-body})

(defn user-patch
  "Handle a HTTP PATCH request with path and body parameters and update an existing user."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))

  (def id (get-in request [:path-params :id]))
  (def email (get-in request [:body-params :email]))

  (if (zero? (db/update-user-email! {:email email :id id}))
    (do
      (log/info "[user-patch] user" id "NOT FOUND")
      {:status 404
       :body {:data {}
              :links {:all-users (format "http://%1$s:%2$s/api/users" server-name server-port)}}})
    (do
      (log/info "[user-patch] email of user" id "changed to" email)
      {:status 200
       :body {:data {:email email :id id}
              :links {:self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}}})))

(defn user-delete
  "Handle a HTTP DELETE request with path parameters."
  [request]
  (def server-name (get-in request [:server-name]))
  (def server-port (get-in request [:server-port]))
  (def uri (get-in request [:uri]))
  ;; (log/info "[user-delete] uri" uri)

  (def id (get-in request [:path-params :id]))

  (if (zero? (db/delete-user! {:id id}))
    (do
      (log/info "[user-delete] user id =" id "NOT FOUND")
      {:status 404
       :body {:data {}
              :links {:all-users (format "http://%1$s:%2$s/api/users" server-name server-port)}}})
    (do
      (log/info "[user-delete]" "user id =" id "FOUND")
      {:status 200
       :body {:data {:id id}
              :links {:all-users (format "http://%1$s:%2$s/api/users" server-name server-port)}
              :self (format "http://%1$s:%2$s%3$s" server-name server-port uri)}})))

(defn service-routes []
  ["/api"
   {:coercion spec-coercion/coercion
    :muuntaja formats/instance
    :swagger {:id ::api}
    :middleware [;; query-params & form-params
                 parameters/parameters-middleware
                 ;; content-negotiation
                 muuntaja/format-negotiate-middleware
                 ;; encoding response body
                 muuntaja/format-response-middleware
                 ;; exception handling
                 exception/exception-middleware
                 ;; decoding request body
                 muuntaja/format-request-middleware
                 ;; coercing response bodys
                 coercion/coerce-response-middleware
                 ;; coercing request parameters
                 coercion/coerce-request-middleware
                 ;; multipart
                 multipart/multipart-middleware]}

   ;; swagger documentation
   ["" {:no-doc true
        :swagger {:info {:title "Hokuto no Ken unofficial REST API"
                         :description "Hokuto no Ken unofficial REST API, built with Clojure"
                         :version "1.0.0"}}}

    ["/swagger.json"
     {:get (swagger/create-swagger-handler)}]

    ["/api-docs/*"
     {:get (swagger-ui/create-swagger-ui-handler
            {:url "/api/swagger.json"
             :config {:validator-url nil}})}]]

;    ["/ping"
;     {:get (constantly (ok {:message "pong"}))}]

    ;; ["/math"
    ;;  {:swagger {:tags ["math"]}}

    ;;  ["/plus"
    ;;   {:get {:summary "plus with spec query parameters"
    ;;          :parameters {:query {:x int?, :y int?}}
    ;;          :responses {200 {:body {:total pos-int?}}}
    ;;          :handler (fn [{{{:keys [x y]} :query} :parameters}]
    ;;                     {:status 200
    ;;                      :body {:total (+ x y)}})}
    ;;    :post {:summary "plus with spec body parameters"
    ;;           :parameters {:body {:x int?, :y int?}}
    ;;           :responses {200 {:body {:total pos-int?}}}
    ;;           :handler (fn [{{{:keys [x y]} :body} :parameters}]
    ;;                      {:status 200
    ;;                       :body {:total (+ x y)}})}}]]

   ["/characters"
    {:swagger {:tags ["characters"]}
     :get {:summary "Retrieve all characters"
           :handler characters-get
           :responses {200 {:body {:data {:characters seq?}
                                   :links {:last string?
                                           :next string?
                                           :self string?}}}}}}]

   ["/fighting_styles"
    {:swagger {:tags ["fighting_styles"]}
     :get {:summary "Retrieve all fighting styles"
           :handler fighting-styles-get
           :responses {200 {:body {:data {:fighting_styles seq?}
                                   :links {:last string?
                                           :next string?
                                           :self string?}}}}}}]

   ["/users"
    {:swagger {:tags ["users"]}
     :get {:summary "Retrieve paginated users"
           :handler users-get
          ;;  :parameters {:query {:is-admin boolean?}}
           :responses {200 {:body {:data {:users seq?}
                                   :links {:last string?
                                           :next string?
                                           :self string?}}}}}
     :post {:summary "Create a new user"
            :handler users-post
            :parameters {:body {:first_name string? :last_name string? :email string? :pass string?}}
            :responses {201 {:body {:data {:id string?}
                                    :links {:all-users string?
                                            :this-user string?}}}}}}]

   ["/users"
    {:swagger {:tags ["users"]}}
    ["/:id"
     {:get {:summary "Retrieve a particular user"
            :handler user-get
            :parameters {:path {:id string?}}
            :responses {200 {:body {:data {:id string?
                                           :first_name string?
                                           :last_name string?}
                                    :links {}}}
                        404 {:body {:data {}
                                    :links {}}}}}
      :delete {:summary "Delete a user"
               :handler user-delete
               :parameters {:path {:id string?}}
               :responses {200 {:body {:data {:id string?}
                                       :links {:all-users string?}}}
                           404 {:body {:data {}
                                       :links {:all-users string?}}}}}
      :patch {:summary "Update a subset of the fields of an existing user"
              :handler user-patch
              :parameters {:body {:email string?}
                           :path {:id string?}}
              :responses {200 {:body {:data {:id string?}
                                      :links {:self string?}}}
                          404 {:body {:data {}
                                      :links {:all-users string?}}}}}}]]

   ["/files"
    {:swagger {:tags ["files"]}}

    ["/upload"
     {:post {:summary "upload a file"
             :parameters {:multipart {:file multipart/temp-file-part}}
             :responses {200 {:body {:name string?, :size int?}}}
             :handler (fn [{{{:keys [file]} :multipart} :parameters}]
                        {:status 200
                         :body {:name (:filename file)
                                :size (:size file)}})}}]

    ["/download"
     {:get {:summary "downloads a file"
            :swagger {:produces ["image/png"]}
            :handler (fn [_]
                       {:status 200
                        :headers {"Content-Type" "image/png"}
                        :body (-> "public/img/warning_clojure.png"
                                  (io/resource)
                                  (io/input-stream))})}}]]])
