package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
)

// CheckEmptyFieldsAll - checks if there are empty fields in the request body: checks all possible fields
func CheckEmptyFieldsAll(entry ThesaurusEntry, response http.ResponseWriter) *EmptyFieldsResponse {
	return checkEmptyFields(entry, response, true, true)
}

// CheckEmptyFieldsWord - checks if there are empty fields in the request body: only checks `word`
func CheckEmptyFieldsWord(entry ThesaurusEntry, response http.ResponseWriter) *EmptyFieldsResponse {
	return checkEmptyFields(entry, response, false, false)
}

// driver for above guys
func checkEmptyFields(entry ThesaurusEntry, response http.ResponseWriter, checkAntonyms bool, checkSynonyms bool) *EmptyFieldsResponse {
	wordExists := entry.Word == ""

	antonymsExist := false
	if checkAntonyms {
		antonymsExist = entry.Antonyms == nil
	}
	synonymsExist := false
	if checkSynonyms {
		synonymsExist = entry.Synonyms == nil
	}

	if wordExists || antonymsExist || synonymsExist {
		fields := map[string]bool{
			"word": wordExists,
		}
		if checkAntonyms {
			fields["antonyms"] = antonymsExist
		}
		if checkSynonyms {
			fields["synonyms"] = synonymsExist
		}
		response.WriteHeader(http.StatusBadRequest)
		payload := EmptyFieldsResponse{
			MessageResponse: MessageResponse{
				Message: "Empty fields in request",
			},
			Fields: fields,
		}
		return &payload
	}
	return nil
}

// CheckAdminCreds - determines whether the person is me!
func CheckAdminCreds(request *http.Request) *MessageResponse {
	username := request.Header.Get("adminUsername")
	password := request.Header.Get("adminPassword")
	// absolutely brilliant and s e c u r e
	if username != "cole" || password != "cool" {
		payload := MessageResponse{
			Message: "Invalid admin creds",
		}
		return &payload
	}
	return nil
}

// MongoError - helper response for if something went wrong with mongo
func MongoError(err error, cancel context.CancelFunc, response http.ResponseWriter) {
	fmt.Println(err)
	response.WriteHeader(http.StatusBadRequest)
	payload := MessageResponse{
		Message: "Oops!",
	}
	json.NewEncoder(response).Encode(payload)
	cancel()
}
