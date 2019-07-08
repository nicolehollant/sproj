package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// GetAPIInfo - Small debug/"hello world" endpoint.
func GetAPIInfo(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting API info!")
	response.Header().Set("content-type", "application/json")
	response.WriteHeader(http.StatusOK)
	payload := MessageResponse{
		Message: "Hi! This is the api for Cole Hollant's thesaurus for SPROJ.\nBase entries from words.bighugelabs.com.",
	}
	json.NewEncoder(response).Encode(payload)
	return
}
