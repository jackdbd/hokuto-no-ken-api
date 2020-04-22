(ns hokuto-users.interceptor-test
  (:require [clojure.test :refer [deftest is testing]]
            [hokuto-users.interceptor :refer [content-length-json-body-interceptor]]))

(deftest interceptor-test
  (testing "has only the :leave handler"
    (is (= true (nil? (:enter content-length-json-body-interceptor))))
    (is (= true (nil? (:error content-length-json-body-interceptor))))
    (is (= false (nil? (:leave content-length-json-body-interceptor))))))

(deftest content-type-test
  (def ctx {:response {:body ""}})
  (def leave-handler (:leave content-length-json-body-interceptor))
  (def res (get-in (leave-handler ctx) [:response]))
  (testing "adds the expected Content-Type header"
    (is (= "application/json;charset=UTF-8" (get-in res [:headers "Content-Type"])))))


(deftest content-length-utf8-empty-string-test
  (def ctx {:response {:body ""}})
  (def leave-handler (:leave content-length-json-body-interceptor))
  (def res (get-in (leave-handler ctx) [:response]))
  (testing "has the expected Content-Length"
    (is (= "2" (get-in res [:headers "Content-Length"])))))


(deftest content-length-utf8-characters-length
  "http://www.i18nguy.com/unicode/supplementary-test.html"
  ; this string has length = 1+2+3+4
  (def ctx {:response {:body "aД中𢳂"}})
  (def leave-handler (:leave content-length-json-body-interceptor))
  (def res (get-in (leave-handler ctx) [:response]))
  (testing "has the expected Content-Length"
    (is (= "12" (get-in res [:headers "Content-Length"])))))
