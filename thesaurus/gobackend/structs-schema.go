package main

import "go.mongodb.org/mongo-driver/bson/primitive"

// ThesaurusEntry - scheme for the thesaurus entry
type ThesaurusEntry struct {
	ID       primitive.ObjectID  `json:"_id,omitempty" bson:"_id,omitempty"`
	Word     string              `json:"word,omitempty" bson:"word,omitempty"`
	Antonyms map[string][]string `json:"antonyms,omitempty" bson:"antonyms,omitempty"`
	Synonyms map[string][]string `json:"synonyms,omitempty" bson:"synonyms,omitempty"`
}
