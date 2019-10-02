package endpoints

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"github.com/colehollant/sproj/thesaurus/backend/app/utils"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

/*
SAMPLE JSON:
"abate": [
    {
      "associations": [],
      "sense": [
        "nonincrease"
      ],
      "word": "abate"
    },
    {
      "associations": [],
      "sense": [
        "discount"
      ],
      "word": "abate"
    }
	],

SCHEMA:
type SenseLevelEntry struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Word      string             `json:"word,omitempty" bson:"word,omitempty"`
	SenseList []SenseLevelData   `json:"senselist,omitempty" bson:"senselist,omitempty"`
}
type SenseLevelData struct {
	Associations []string `json:"associations,omitempty" bson:"associations,omitempty"`
	Sense        []string `json:"sense,omitempty" bson:"sense,omitempty"`
}
*/

func checkEmptyFields(entry structs.SenseLevelEntry, response http.ResponseWriter) *structs.MessageResponse {
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

// respondJSON makes the response with payload as json format
func respondJSON(w http.ResponseWriter, status int, payload interface{}) {
	inner, err := json.Marshal(payload)
	response := []byte(`{"message": "Success!", "data":`)
	closeBrackets := []byte(`}`)
	response = append(response, append(inner, closeBrackets...)...)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write([]byte(response))
}

// respondError makes the error response with payload as json format
func respondError(w http.ResponseWriter, code int, message string) {
	respondJSON(w, code, map[string]string{"error": message})
}

// CreateSenseLevel - Add entries to the collection!
func CreateSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating word!")
	entry := structs.SenseLevelEntry{}

	decoder := json.NewDecoder(request.Body)
	if err := decoder.Decode(&entry); err != nil {
		respondError(response, http.StatusBadRequest, err.Error())
		return
	}
	defer request.Body.Close()

	wordExists := checkEmptyFields(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	respondJSON(response, http.StatusCreated, entry)

	// createdWord := entry.Word

	// wordExists := checkEmptyFields(entry, response)
	// if wordExists != nil {
	// 	json.NewEncoder(response).Encode(wordExists)
	// 	return
	// }

	// collection := client.Database("thesaurus-v1").Collection("words")
	// ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	// exists := collection.FindOne(ctx, structs.ThesaurusEntry{Word: createdWord}).Decode(&entry)

	// if exists == nil {
	// 	response.WriteHeader(http.StatusBadRequest)
	// 	payload := structs.MessageResponse{
	// 		Message: "Word already exists",
	// 	}
	// 	json.NewEncoder(response).Encode(payload)
	// 	cancel()
	// 	return
	// }

	// result, err := collection.InsertOne(ctx, entry)
	// if err != nil {
	// 	utils.MongoError(err, cancel, response)
	// 	return
	// }

	// response.WriteHeader(http.StatusCreated)
	// payload := structs.CreateWordSuccess{
	// 	MessageResponse: structs.MessageResponse{
	// 		Message: "Word added",
	// 	},
	// 	Data: structs.CreateWordSuccessData{
	// 		Word:   createdWord,
	// 		Result: result,
	// 	},
	// }

	// json.NewEncoder(response).Encode(payload)
	// cancel()
	// return
}

// GetAllSenseLevels - Add entries to the collection!
func GetAllSenseLevels(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	cursor, err := collection.Find(ctx, bson.D{})

	if err != nil {
		utils.MongoError(err, cancel, response)
		return
	}
	var s []string

	for cursor.Next(ctx) {
		elem := &bson.D{}
		err = cursor.Decode(elem)
		if err != nil {
			utils.MongoError(err, cancel, response)
			return
		}
		word := elem.Map()["word"].(string)
		s = append(s, word)
	}
	fmt.Println("guess we good")
	response.WriteHeader(http.StatusOK)
	payload := structs.GetAllWordsSuccess{
		MessageResponse: structs.MessageResponse{
			Message: "Words aggregated",
		},
		Data: structs.GetAllWordsSuccessData{
			Result: s,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}

// UpdateSenseLevel - Update entries in the collection!
func UpdateSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	var entry structs.SenseLevelEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := checkEmptyFields(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, structs.ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.ReplaceOne(ctx, structs.ThesaurusEntry{Word: createdWord}, entry)
	if err != nil {
		utils.MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := structs.UpdateWordSuccess{
		MessageResponse: structs.MessageResponse{
			Message: "Word updated",
		},
		Data: structs.UpdateWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}

// DeleteSenseLevel - Remove entries from the collection!
func DeleteSenseLevel(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	var entry structs.ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := utils.CheckEmptyFieldsWord(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, structs.ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.DeleteOne(ctx, structs.ThesaurusEntry{Word: createdWord})
	if err != nil {
		utils.MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := structs.DeleteWordSuccess{
		MessageResponse: structs.MessageResponse{
			Message: "Word removed",
		},
		Data: structs.DeleteWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}
