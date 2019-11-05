package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"go.mongodb.org/mongo-driver/mongo"
)

func checkEmptyFieldsVAD(entry structs.VADEntry, response http.ResponseWriter) *structs.MessageResponse {
	fmt.Println(entry.Word)
	return utils.CheckEmptyFieldsAllGeneral(entry.Word == "" || entry.Valence == "" || entry.Arousal == "" || entry.Dominance == "", response)
}

// CreateVAD - Add entries to the collection!
func CreateVAD(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating VAD!")
	entry := structs.VADEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := checkEmptyFieldsVAD(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("vad")
	utils.CreateEntry(entry, structs.Filter{Word: entry.Word}, collection, response)
}

// GetAllVADs - Add entries to the collection!
func GetAllVADs(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("vad")
	utils.AggregateEntries("word", collection, response)
}

// UpdateVAD - Update entries in the collection!
func UpdateVAD(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	entry := structs.VADEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := checkEmptyFieldsVAD(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("vad")
	utils.ReplaceEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}

// DeleteVAD - Remove entries from the collection!
func DeleteVAD(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	entry := structs.VADEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := utils.CheckEmptyFieldsAllGeneral(createdWord == "", response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("vad")
	utils.DeleteEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}
