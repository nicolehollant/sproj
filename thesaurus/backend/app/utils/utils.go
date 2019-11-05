package utils

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// RespondJSON -- create a response with json marshalled from interface
func RespondJSON(w http.ResponseWriter, status int, payload interface{}, messageOptional ...string) {
	message := "Success!"
	if len(messageOptional) > 0 {
		message = messageOptional[0]
	}
	inner, err := json.Marshal(payload)
	response := fmt.Sprintf(`{ "message": "%s", "data": %s }`, message, inner)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write([]byte(response))
}

// RespondError -- sends an error response
func RespondError(w http.ResponseWriter, code int, message string) {
	RespondJSON(w, code, map[string]string{"error": message}, "Error!")
}

// CheckEmptyFieldsAllGeneral - checks if there are empty fields in the request body: checks all possible fields
func CheckEmptyFieldsAllGeneral(empty bool, response http.ResponseWriter) *structs.MessageResponse {
	if empty {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Empty fields in request",
		}
		return &payload
	}
	return nil
}

// CursorIsEmpty -- Check if cursor is empty
func CursorIsEmpty(cursor *mongo.Cursor) bool {
	return !cursor.Next(context.Background())
}

// CursorLength -- Find length of cursor
func CursorLength(cursor *mongo.Cursor) int {
	i := 0
	for cursor.Next(context.Background()) {
		i++
	}
	return i
}

// CheckAdminCreds - determines whether the person is me!
func CheckAdminCreds(request *http.Request) *structs.MessageResponse {
	username := request.Header.Get("adminUsername")
	password := request.Header.Get("adminPassword")
	// absolutely brilliant and s e c u r e
	if username != "cole" || password != "cool" {
		payload := structs.MessageResponse{
			Message: "Invalid admin creds",
		}
		return &payload
	}
	return nil
}

// MongoError - helper response for if something went wrong with mongo
func MongoError(err error, cancel context.CancelFunc, response http.ResponseWriter) {
	fmt.Println(err)
	response.WriteHeader(http.StatusBadRequest)
	payload := structs.MessageResponse{
		Message: "Oops!",
	}
	json.NewEncoder(response).Encode(payload)
	cancel()
}

// CheckExists -- determints if a word exists or not
func CheckExists(ctx context.Context, item interface{}, collection *mongo.Collection, response http.ResponseWriter) error {
	cursor, err := collection.Find(ctx, item)

	if err != nil || CursorIsEmpty(cursor) {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word does not already exist",
		}
		json.NewEncoder(response).Encode(payload)
		return fmt.Errorf("Word does not already exist: %s", err)
	}
	return nil
}

// CheckNotExists -- determints if a word exists or not
func CheckNotExists(ctx context.Context, item interface{}, collection *mongo.Collection, response http.ResponseWriter) error {
	cursor, err := collection.Find(ctx, item)

	if err != nil || !CursorIsEmpty(cursor) {
		response.WriteHeader(http.StatusBadRequest)
		payload := structs.MessageResponse{
			Message: "Word exists",
		}
		if err != nil {
			fmt.Sprintf("Word exists: %s", err)
			payload = structs.MessageResponse{
				Message: fmt.Sprintf("Word exists: %s", err),
			}
		}
		json.NewEncoder(response).Encode(payload)
		return fmt.Errorf("Word exists: %s", err)
	}
	return nil
}

// UnmarshalEntry -- wraps unmarshalling
func UnmarshalEntry(entry interface{}, response http.ResponseWriter, request *http.Request) error {
	if err := json.NewDecoder(request.Body).Decode(&entry); err != nil && err != io.EOF {
		RespondError(response, http.StatusBadRequest, err.Error())
		return err
	}
	defer request.Body.Close()
	return nil
}

// CreateEntry -- helper to gather stuff from mongo by key
func CreateEntry(entry interface{}, filter interface{}, collection *mongo.Collection, response http.ResponseWriter) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

	fmt.Printf("Filter is: %s\n", filter)
	err := CheckNotExists(ctx, filter, collection, response)

	if err != nil {
		cancel()
		return
	}

	_, err = collection.InsertOne(ctx, entry)
	if err != nil {
		MongoError(err, cancel, response)
		return
	}
	cancel()
	fmt.Println("Entry is: %s", entry)
	RespondJSON(response, http.StatusCreated, entry)
}

// AggregateEntries -- helper to gather stuff from mongo by key
func AggregateEntries(key string, collection *mongo.Collection, response http.ResponseWriter) {
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
		word := elem.Map()[key].(string)
		s = append(s, word)
	}

	cancel()
	type Res struct {
		Result []string `json:"result"`
	}
	RespondJSON(response, http.StatusOK, Res{Result: s})
}

// ReplaceEntry -- helper to gather stuff from mongo by key
func ReplaceEntry(entry interface{}, filter interface{}, collection *mongo.Collection, response http.ResponseWriter) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

	err := CheckExists(ctx, filter, collection, response)

	if err != nil {
		cancel()
		return
	}

	result, err := collection.ReplaceOne(ctx, filter, entry, options.Replace().SetUpsert(false))
	if err != nil {
		MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	type Res struct {
		Result mongo.UpdateResult `json:"result"`
	}
	cancel()
	RespondJSON(response, http.StatusOK, Res{Result: *result})
}

// DeleteEntry -- helper to gather stuff from mongo by key
func DeleteEntry(entry interface{}, filter interface{}, collection *mongo.Collection, response http.ResponseWriter) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

	err := CheckExists(ctx, filter, collection, response)

	if err != nil {
		cancel()
		return
	}

	result, err := collection.DeleteOne(ctx, filter)
	if err != nil {
		MongoError(err, cancel, response)
		return
	}

	response.WriteHeader(http.StatusOK)
	type Res struct {
		Result mongo.DeleteResult `json:"result"`
	}
	cancel()
	RespondJSON(response, http.StatusOK, Res{Result: *result})
}

// FindOneEntry -- find and return one entry... currently kinda busted
func FindOneEntry(entry interface{}, filter interface{}, collection *mongo.Collection, response http.ResponseWriter) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

	err := CheckExists(ctx, filter, collection, response)

	if err != nil {
		cancel()
		return
	}

	err = collection.FindOne(ctx, filter).Decode(&entry)
	if err != nil {
		MongoError(err, cancel, response)
		return
	}
	fmt.Println(entry)
	cancel()
	RespondJSON(response, http.StatusOK, entry)
}
