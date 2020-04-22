(ns hokuto-users.interceptor
  (:require [cheshire.core :as json]
            [io.pedestal.interceptor :as interceptor]))

(def content-length-json-body-interceptor
  "Interceptor to coerce :body into a JSON string.

  This interceptor also adds Content-Type and Content-Length HTTP headers.
  [Unicode table](https://unicode-table.com/en/)
  [UTF-8](https://en.wikipedia.org/wiki/UTF-8)"
  (interceptor/interceptor
   {:name ::content-length-json-body-interceptor
    :leave (fn [context]
             (let [response (:response context)
                   body (:body response)
                   json-response-body (if body (json/generate-string body) "")
                    ;; Content-Length is the size of the response in bytes.
                    ;; Let's count the bytes instead of the string, in case
                    ;; there are unicode characters (e.g. chinese ideograms).
                   content-length (count (.getBytes ^String json-response-body))
                   headers (:headers response {})]
               ; HTTP headers added by this interceptor.
               (def new-headers {"Content-Type" "application/json;charset=UTF-8"
                                 "Content-Length" (str content-length)})
               (assoc context
                      :response {:status (:status response)
                                 :body json-response-body
                                 :headers (merge headers new-headers)})))}))
