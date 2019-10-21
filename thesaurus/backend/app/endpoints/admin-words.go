package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"go.mongodb.org/mongo-driver/mongo"
)

// driver for above guys
func checkEmptyFieldsWordLevel(entry structs.ThesaurusEntry, response http.ResponseWriter) *structs.MessageResponse {
	return utils.CheckEmptyFieldsAllGeneral(
		entry.Word == "" ||
			entry.Antonyms == nil ||
			entry.Synonyms == nil ||
			len(entry.Antonyms) == 0 ||
			len(entry.Synonyms) == 0,
		response)
}

// CreateWord - Add entries to the collection!
func CreateWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating word!")
	entry := structs.ThesaurusEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := checkEmptyFieldsWordLevel(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	utils.CreateEntry(entry, structs.ThesaurusEntry{Word: entry.Word}, collection, response)
}

// GetAllWords - Add entries to the collection!
func GetAllWords(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	utils.AggregateEntries("word", collection, response)
}

// UpdateWord - Update entries in the collection!
func UpdateWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	entry := structs.ThesaurusEntry{}
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

	wordExists := checkEmptyFieldsWordLevel(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	utils.ReplaceEntry(entry, structs.ThesaurusEntry{Word: createdWord}, collection, response)
}

// DeleteWord - Remove entries from the collection!
func DeleteWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	entry := structs.ThesaurusEntry{}
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

	collection := client.Database("thesaurus-v1").Collection("words")
	utils.DeleteEntry(entry, structs.ThesaurusEntry{Word: createdWord}, collection, response)
}
