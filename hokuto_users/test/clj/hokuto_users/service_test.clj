(ns hokuto-users.service-test
  (:require [cheshire.core :as json]
            [clojure.test :refer [deftest is testing]]
            [hokuto-users.service :as service :refer [home-page]]
            [io.pedestal.http :as http]
            [io.pedestal.test :refer [response-for]]))

(def http-service
  "Create a servlet with the provided service map."
  (::http/service-fn (http/create-servlet service/service-map)))

(def common-headers
  "HTTP headers shared across the responses of all service routes."
  {"Content-Security-Policy" "object-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:;"
   "Content-Type" "application/json;charset=UTF-8"
   "Strict-Transport-Security" "max-age=31536000; includeSubdomains"
   "X-Content-Type-Options" "nosniff"
   "X-Download-Options" "noopen"
   "X-Frame-Options" "DENY"
   "X-Permitted-Cross-Domain-Policies" "none"
   "X-XSS-Protection" "1; mode=block"})

; This tests just the Ring response map, that at this point has no HTTP headers,
; nor Pedestal interceptors applied to it.
(deftest response
  (def res (home-page {}))
  (testing "has the expected status"
    (is (= 200 (get-in res [:status]))))
  (testing "has no HTTP headers"
    (is (= {} (:headers res))))
  (testing "has the expected body"
    (is (= "world" (get-in res [:body :hello])))))

; This tests the Pedestal HTTP service (that returns a JSON).
(deftest home-route-test
  (def res (response-for http-service :get "/"))
  (testing "responds with the expected JSON"
    (is (=
         {"hello" "world"}
         (json/parse-string (:body res)))))
  (testing "responds with the expected HTTP headers"
    (is (=
         common-headers
         (:headers res))))
  (testing "responds with the expected JSON given the `name` query parameter"
    (def res (response-for http-service :get "/?name=jack"))
    (is (=
         {"hello" "jack"}
         (json/parse-string (:body res))))))

(deftest about-route-test
  (def res (response-for http-service :get "/about"))
  (testing "response contains expected Clojure version"
    (is (.contains
       (:body res)
       "Clojure 1.10")))
  (testing "responds with the expected HTTP headers"
    (is (=
         (merge common-headers {"Content-Length" 59})
         (:headers res)))))

(deftest users-get-test
  (def res (response-for http-service :get "/users"))
  ; (prn "USERS GET TEST" res)
  (testing "responds with HTTP 200 (Ok)"
    (is (= 200 (:status res))))
  (testing "responds with the expected Content-Type header"
    (is (=
         "application/json;charset=UTF-8"
         (get-in res [:headers "Content-Type"]))))
  (comment
    (testing "contains a Content-Length header"
      (is
       (contains? (:headers res) "Content-Length")
       "Content-Length header is missing"))))

(deftest users-post-test
  (def res (response-for http-service
                         :post "/users"
                         ;; Set Content-Type so body-params can parse the body
                         :headers {"Content-Type" "application/json"}
                         :body (json/encode {:age 99 :name "jack"})))
  (testing "responds with HTTP 201 (Created)"
    (is (= 201 (:status res))))
  (testing "responds with Location header"
    (is (contains? (:headers res) "Location")))
  (testing "responds with expected JSON response"
    (is (=
         {"age" 99 "name" "jack"}
         (json/parse-string (:body res))))))

(deftest user-get-test
  (def res (response-for http-service
                         :post "/users"
                         :headers {"Content-Type" "application/json"}
                         :body (json/encode {:age 22 :name "bob"})))
  (def location-url (get-in res [:headers "Location"]))
  (testing "responds with HTTP 200 (Ok) for an existing user"
    (def res (response-for http-service :get location-url))
    (is (= 200 (:status res))))
  (testing "responds with HTTP 404 (Not Found) for a non-existing user"
    (def res (response-for http-service :get "/users/some-non-existing-user"))
    (is (= 404 (:status res)))))
