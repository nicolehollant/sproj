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

// CreateWord - Add entries to the collection!
func CreateWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating word!")
	var entry structs.ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := utils.CheckEmptyFieldsAll(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, structs.ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists == nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word already exists",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.InsertOne(ctx, entry)
	if err != nil {
		utils.MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusCreated)
	payload := structs.CreateWordSuccess{
		MessageResponse: structs.MessageResponse{
			Message: "Word added",
		},
		Data: structs.CreateWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
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

// UpdateWord - Update entries in the collection!
func UpdateWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	var entry structs.ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := utils.CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := utils.CheckEmptyFieldsAll(entry, response)
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

// DeleteWord - Remove entries from the collection!
func DeleteWord(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
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
