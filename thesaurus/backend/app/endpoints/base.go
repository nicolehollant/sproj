package endpoints

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/colehollant/sproj/thesaurus/backend/app/structs"
)

// GetAPIInfo - Small debug/"hello world" endpoint.
func GetAPIInfo(response http.ResponseWriter, request *http.Request) {
	fmt.Println("Getting API info!")
	response.WriteHeader(http.StatusOK)
	payload := structs.MessageResponse{
		Message: "Hi! This is the api for Cole Hollant's thesaurus for SPROJ.\nBase entries from words.bighugelabs.com.",
	}
	json.NewEncoder(response).Encode(payload)
	return
}
