package structs

import "go.mongodb.org/mongo-driver/mongo"

// GetAllWordsSuccessData - Data for GetAllWordsSuccess: list of all words
type GetAllWordsSuccessData struct {
	Result []string `json:"result"`
}

// GetAllWordsSuccess - Response upon getting all words
type GetAllWordsSuccess struct {
	MessageResponse
	Data GetAllWordsSuccessData `json:"data"`
}

// DeleteWordSuccessData - Data for DeleteWordSuccess: mongo's result
type DeleteWordSuccessData struct {
	Word   string              `json:"word"`
	Result *mongo.DeleteResult `json:"result"`
}

// DeleteWordSuccess - Response upon deleting a word
type DeleteWordSuccess struct {
	MessageResponse
	Data DeleteWordSuccessData `json:"data"`
}

// UpdateWordSuccessData - Data for UpdateWordSuccess: mongo's result
type UpdateWordSuccessData struct {
	Word   string              `json:"word"`
	Result *mongo.UpdateResult `json:"result"`
}

// UpdateWordSuccess - Response upon updating a word
type UpdateWordSuccess struct {
	MessageResponse
	Data UpdateWordSuccessData `json:"data"`
}

// CreateWordSuccessData - Data for CreateWordSuccess: mongo's result
type CreateWordSuccessData struct {
	Word   string                 `json:"word"`
	Result *mongo.InsertOneResult `json:"result"`
}

// CreateWordSuccess - Response upon creating a word
type CreateWordSuccess struct {
	MessageResponse
	Data CreateWordSuccessData `json:"data"`
}

// GetWordSuccessData - Data for GetWordSuccess: word that is retrieved
type GetWordSuccessData struct {
	Word   string         `json:"word"`
	Result ThesaurusEntry `json:"result"`
}

// GetWordSuccess - Response upon retrieving a word
type GetWordSuccess struct {
	MessageResponse
	Data GetWordSuccessData `json:"data"`
}

// EmptyFieldsResponse - Response upon encountering empty fields
type EmptyFieldsResponse struct {
	MessageResponse
	Fields map[string]bool `json:"fields"`
}

// MessageResponse - Response with a message
type MessageResponse struct {
	Message string `json:"message"`
}
