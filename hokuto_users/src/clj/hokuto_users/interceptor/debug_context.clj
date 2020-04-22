(ns hokuto-users.interceptor.debug-context
  "Namespace for interceptors useful for debugging.")

(defn- enter-debug-context-map
  "Extract the `:request` from the `context` map and print it."
  [{:keys [request] :as context}]
  (prn "===>" :REQUEST request)
  ; (prn "==> enter-debug" (dissoc context
  ;                                :async?
  ;                                :bindings
  ;                                :enter-async
  ;                                :io.pedestal.interceptor.chain/execution-id
  ;                                :io.pedestal.interceptor.chain/queue
  ;                                :io.pedestal.interceptor.chain/stack
  ;                                :io.pedestal.interceptor.chain/terminators
  ;                                :request
  ;                                :response
  ;                                :route
  ;                                :servlet
  ;                                :servlet-config
  ;                                :servlet-request
  ;                                :servlet-response
  ;                                :url-for))
  ; (prn "===> INTERCEPTORS for this route" (get-in context [:route :interceptors]))
  context)

(defn- leave-debug-context-map
  "Extract the `:response` from the `context` map and print it."
  [{:keys [response] :as context}]
  (prn "<===" :RESPONSE response)
  context)

(def debug-context-map
  "Debug interceptor."
  {:name ::debug-context-map
   :enter enter-debug-context-map
   :leave leave-debug-context-map})
