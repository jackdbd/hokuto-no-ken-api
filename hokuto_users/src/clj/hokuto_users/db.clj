(ns hokuto-users.db)

(defonce database (atom {}))

(defn db-seed
  []
  (swap! database assoc :111a775f-4914-4ea2-b0b7-9659acd9bf5e "bob")
  (swap! database assoc :d9adeb50-61c1-48c9-a2f9-697abf657ec0 "john")
  (swap! database assoc :dda16a5f-aa90-4c68-a363-6c6cfb7e38ff "susy"))

(defn db-reset
  []
  (reset! database {}))

(defn db-read
  []
  @database)
