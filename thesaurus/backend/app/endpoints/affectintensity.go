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

// GetAffectIntensity - Access entries in the collection!
func GetAffectIntensity(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting word!")
	word := mux.Vars(request)["word"]

	entry := structs.AffectIntensityEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := utils.CheckEmptyFieldsAllGeneral(word == "", response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("affectintensity")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	err = collection.FindOne(ctx, structs.Filter{Word: word}).Decode(&entry)

	if err != nil {
		cancel()
		utils.RespondError(response, http.StatusBadRequest, "Word does not already exist")
		return
	}

	cancel()
	utils.RespondJSON(response, http.StatusOK, entry)
}
