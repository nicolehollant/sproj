package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"go.mongodb.org/mongo-driver/mongo"
)

/*

{
    "word": "testword",
    "AffectList": [
    	{
    		"sense": [
    			"lorem",
    			"ipsum"
    		],
    		"associations": [
    			"dolor",
    			"sit"
    		]
    	},
    	{
    		"sense": [
    			"consectetur"
    		],
    		"associations": [
    			"adipiscing",
    			"elit"
    		]
    	}
    ]

}

{
	"word": "abandon",
	"affectlist": [
		{
      "affect_dimension": "fear",
      "score": "0.531"
    },
    {
      "affect_dimension": "sadness",
      "score": "0.703"
    }
	]
}

"abandon": [
    {
      "affect_dimension": "fear",
      "score": "0.531",
      "word": "abandon"
    },
    {
      "affect_dimension": "sadness",
      "score": "0.703",
      "word": "abandon"
    }
  ]
*/

func checkEmptyFieldsAffectIntensity(entry structs.AffectIntensityEntry, response http.ResponseWriter) *structs.MessageResponse {
	fmt.Println(entry.Word)
	fmt.Println(entry.AffectList)
	emptyAffectList := false
	for _, x := range entry.AffectList {
		if x.AffectDimension == "" || x.Score == "" {
			emptyAffectList = true
			break
		}
	}
	return utils.CheckEmptyFieldsAllGeneral(entry.Word == "" || entry.AffectList == nil || emptyAffectList, response)
}

// CreateAffectIntensity - Add entries to the collection!
func CreateAffectIntensity(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating AffectIntensity!")
	entry := structs.AffectIntensityEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := checkEmptyFieldsAffectIntensity(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("affectintensity")
	utils.CreateEntry(entry, structs.Filter{Word: entry.Word}, collection, response)
}

// GetAllAffectIntensitys - Add entries to the collection!
func GetAllAffectIntensitys(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("affectintensity")
	utils.AggregateEntries("word", collection, response)
}

// UpdateAffectIntensity - Update entries in the collection!
func UpdateAffectIntensity(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	entry := structs.AffectIntensityEntry{}
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

	wordExists := checkEmptyFieldsAffectIntensity(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("affectintensity")
	utils.ReplaceEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}

// DeleteAffectIntensity - Remove entries from the collection!
func DeleteAffectIntensity(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	entry := structs.AffectIntensityEntry{}
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

	collection := client.Database("thesaurus-v1").Collection("affectintensity")
	utils.DeleteEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}
