package main

import (
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/problem", problemHandler)

	log.Fatal(http.ListenAndServe(":8080", nil))
}

func problemHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Write([]byte(`{
		"id":"e3y52hu1",
		"type":"algebra",
		"question":"x + 1 = 5",
		"answer":"4"
	}`))
}
