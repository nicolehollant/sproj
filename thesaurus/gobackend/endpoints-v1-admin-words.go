package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"go.mongodb.org/mongo-driver/bson"
)

// CreateWord - Add entries to the collection!
func CreateWord(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Creating word!")
	var entry ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := CheckEmptyFieldsAll(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists == nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := MessageResponse{
			Message: "Word already exists",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.InsertOne(ctx, entry)
	if err != nil {
		MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusCreated)
	payload := CreateWordSuccess{
		MessageResponse: MessageResponse{
			Message: "Word added",
		},
		Data: CreateWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}

// GetAllWords - Add entries to the collection!
func GetAllWords(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting words!")

	hasCreds := CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	cursor, err := collection.Find(ctx, bson.D{})

	if err != nil {
		MongoError(err, cancel, response)
		return
	}
	var s []string

	for cursor.Next(ctx) {
		elem := &bson.D{}
		err = cursor.Decode(elem)
		if err != nil {
			MongoError(err, cancel, response)
			return
		}
		word := elem.Map()["word"].(string)
		s = append(s, word)
	}
	fmt.Println("guess we good")
	response.WriteHeader(http.StatusOK)
	payload := GetAllWordsSuccess{
		MessageResponse: MessageResponse{
			Message: "Words aggregated",
		},
		Data: GetAllWordsSuccessData{
			Result: s,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}

// UpdateWord - Update entries in the collection!
func UpdateWord(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Updating word!")
	var entry ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := CheckEmptyFieldsAll(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.ReplaceOne(ctx, ThesaurusEntry{Word: createdWord}, entry)
	if err != nil {
		MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := UpdateWordSuccess{
		MessageResponse: MessageResponse{
			Message: "Word updated",
		},
		Data: UpdateWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}

// DeleteWord - Remove entries from the collection!
func DeleteWord(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Deleting word!")
	var entry ThesaurusEntry
	_ = json.NewDecoder(request.Body).Decode(&entry)

	hasCreds := CheckAdminCreds(request)
	if hasCreds != nil {
		json.NewEncoder(response).Encode(hasCreds)
		return
	}

	createdWord := entry.Word

	wordExists := CheckEmptyFieldsWord(entry, response)
	if wordExists != nil {
		json.NewEncoder(response).Encode(wordExists)
		return
	}

	collection := client.Database("thesaurus-v1").Collection("words")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	exists := collection.FindOne(ctx, ThesaurusEntry{Word: createdWord}).Decode(&entry)

	if exists != nil {
		response.WriteHeader(http.StatusBadRequest)
		payload := MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		cancel()
		return
	}

	result, err := collection.DeleteOne(ctx, ThesaurusEntry{Word: createdWord})
	if err != nil {
		MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	payload := DeleteWordSuccess{
		MessageResponse: MessageResponse{
			Message: "Word removed",
		},
		Data: DeleteWordSuccessData{
			Word:   createdWord,
			Result: result,
		},
	}

	json.NewEncoder(response).Encode(payload)
	cancel()
	return
}
