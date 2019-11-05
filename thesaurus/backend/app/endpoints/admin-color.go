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

# POST LIKE THIS
{
    "word": "abandoned",
    "colorlist": [
        { "color": "black", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3" },
        { "color": "grey", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3" },
        { "color": "black", "sense": [ "neglect" ], "totalvotes": "9", "votes": "6" }
    ]
}

# PARSE FROM THIS
"abandoned": [
    { "color": "black", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3", "word": "abandoned" },
    { "color": "grey", "sense": [ "seclusion" ], "totalvotes": "10", "votes": "3", "word": "abandoned" },
    { "color": "black", "sense": [ "neglect" ], "totalvotes": "9", "votes": "6", "word": "abandoned" }
  ],

// ColorEntry - scheme for color
type ColorEntry struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Word      string             `json:"word,omitempty" bson:"word,omitempty"`
	ColorList []ColorData        `json:"colorlist,omitempty" bson:"colorlist,omitempty"`
}

// ColorData - scheme for color data
type ColorData struct {
	Color      string              `json:"color,omitempty" bson:"color,omitempty"`
	Totalvotes string              `json:"totalvotes,omitempty" bson:"totalvotes,omitempty"`
	Votes      string              `json:"votes,omitempty" bson:"votes,omitempty"`
	Sense      map[string][]string `json:"associations,omitempty" bson:"associations,omitempty"`
}
*/

func checkEmptyFieldsColor(entry structs.ColorEntry, response http.ResponseWriter) *structs.MessageResponse {
	fmt.Println(entry.Word)
	fmt.Println(entry.ColorList)
	emptyColorList := false
	for _, x := range entry.ColorList {
		if x.Color == "" || x.Sense == nil || x.Totalvotes == "" || x.Votes == "" {
			emptyColorList = true
			break
		}
	}
	return utils.CheckEmptyFieldsAllGeneral(entry.Word == "" || entry.ColorList == nil || emptyColorList, response)
}

// CreateColor - Add entries to the collection!
func CreateColor(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating Color!")
	entry := structs.ColorEntry{}
	err := utils.UnmarshalEntry(&entry, response, request)
	if err != nil {
		return
	}

	wordExists := checkEmptyFieldsColor(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("color")
	utils.CreateEntry(entry, structs.Filter{Word: entry.Word}, collection, response)
}

// GetAllColors - Add entries to the collection!
func GetAllColors(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("color")
	utils.AggregateEntries("word", collection, response)
}

// UpdateColor - Update entries in the collection!
func UpdateColor(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	entry := structs.ColorEntry{}
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

	wordExists := checkEmptyFieldsColor(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("color")
	utils.ReplaceEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}

// DeleteColor - Remove entries from the collection!
func DeleteColor(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	entry := structs.ColorEntry{}
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

	collection := client.Database("thesaurus-v1").Collection("color")
	utils.DeleteEntry(entry, structs.Filter{Word: createdWord}, collection, response)
}
