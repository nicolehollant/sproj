package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
	"go.mongodb.org/mongo-driver/mongo"
)

// GetAPIInfo - Small debug/"hello world" endpoint.
func GetAPIInfo(client *mongo.Client, response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting API info!")
	response.WriteHeader(http.StatusOK)
	payload := structs.MessageResponse{
		Message: "Hi! This is the api for Cole Hollant's thesaurus for SPROJ.\nBase entries from words.bighugelabs.com.",
	}
	json.NewEncoder(response).Encode(payload)
	return
}
