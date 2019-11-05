package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sort"

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

func extendSet(a []string, b []string) []string {

	check := make(map[string]int)
	d := append(a, b...)
	res := make([]string, 0)
	for _, val := range d {
		check[val] = 1
	}

	for letter, _ := range check {
		res = append(res, letter)
	}
	sort.Strings(res)
	return res
}

func addWordLevel(entry *structs.SenseLevelEntry) {
	// entry.Name = "Paul"
	var wordLevelAssociations []string
	var wordLevelSense []string
	for _, x := range entry.SenseList {
		wordLevelAssociations = extendSet(wordLevelAssociations, x.Associations)
		wordLevelSense = extendSet(wordLevelSense, x.Sense)
	}
	entry.WordLevel = structs.SenseLevelData{
		Associations: wordLevelAssociations,
		Sense:        wordLevelSense,
	}
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
	addWordLevel(&entry)
	collection := client.Database("thesaurus-v1").Collection("senselevel")
	// utils.CreateEntry(entry, structs.SenseLevelEntry{Word: entry.Word}, collection, response)
	utils.CreateEntry(entry, structs.Filter{Word: entry.Word}, collection, response)
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
	utils.ReplaceEntry(entry, structs.Filter{Word: createdWord}, collection, response)
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
	utils.DeleteEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}
