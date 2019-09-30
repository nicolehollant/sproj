package endpoints

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

// GetWord - Access entries in the collection!
func GetWord(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting word!")
	var entry ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	params := mux.Vars(request)
	word := params["word"]
	entry.Word = word

	wordExists := CheckEmptyFieldsWord(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, ThesaurusEntry{Word: word}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := GetWordSuccess{
		MessageResponse: MessageResponse{
			Message: "Word retrieved",
		},
		Data: GetWordSuccessData{
			Word:   word,
			Result: entry,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}
