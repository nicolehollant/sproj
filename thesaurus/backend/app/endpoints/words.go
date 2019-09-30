package endpoints

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
)

// GetWord - Access entries in the collection!
func GetWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting word!")
	var entry structs.ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	params := mux.Vars(request)
	word := params["word"]
	entry.Word = word

	wordExists := utils.CheckEmptyFieldsWord(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, structs.ThesaurusEntry{Word: word}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := structs.GetWordSuccess{
		MessageResponse: structs.MessageResponse{
			Message: "Word retrieved",
		},
		Data: structs.GetWordSuccessData{
			Word:   word,
			Result: entry,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}
