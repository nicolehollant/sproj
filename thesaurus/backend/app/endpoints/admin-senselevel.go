package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"go.mongodb.org/mongo-driver/mongo"
)

func checkEmptyFieldsSenseLevel(entry structs.SenseLevelEntry, response http.ResponseWriter) *structs.MessageResponse {
	fmt.Println(entry.Word)
	fmt.Println(entry.SenseList)
	emptySenseList := false
	for _, x := range entry.SenseList {
		if x.Associations == nil || x.Sense == nil {
			emptySenseList = true
			break
		}
	}
	return utils.CheckEmptyFieldsAllGeneral(entry.Word == "" || entry.SenseList == nil || emptySenseList, response)
}

// CreateSenseLevel - Add entries to the collection!
func CreateSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating senselevel!")
	entry := structs.SenseLevelEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := checkEmptyFieldsSenseLevel(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("senselevel")
	utils.CreateEntry(entry, structs.SenseLevelEntry{Word: entry.Word}, collection, response)
}

// GetAllSenseLevels - Add entries to the collection!
func GetAllSenseLevels(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("senselevel")
	utils.AggregateEntries("word", collection, response)
}

// UpdateSenseLevel - Update entries in the collection!
func UpdateSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	entry := structs.SenseLevelEntry{}
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

	wordExists := checkEmptyFieldsSenseLevel(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("senselevel")
	utils.ReplaceEntry(entry, structs.SenseLevelEntry{Word: createdWord}, collection, response)
}

// DeleteSenseLevel - Remove entries from the collection!
func DeleteSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	entry := structs.SenseLevelEntry{}
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

	collection := client.Database("thesaurus-v1").Collection("senselevel")
	utils.DeleteEntry(entry, structs.SenseLevelEntry{Word: createdWord}, collection, response)
}
