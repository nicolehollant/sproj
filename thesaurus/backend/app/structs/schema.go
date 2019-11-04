package structs

import "go.mongodb.org/mongo-driver/bson/primitive"

// ThesaurusEntry - scheme for the thesaurus entry
type ThesaurusEntry struct {
	ID       primitive.ObjectID  `json:"_id,omitempty" bson:"_id,omitempty"`
	Word     string              `json:"word,omitempty" bson:"word,omitempty"`
	Antonyms map[string][]string `json:"antonyms,omitempty" bson:"antonyms,omitempty"`
	Synonyms map[string][]string `json:"synonyms,omitempty" bson:"synonyms,omitempty"`
}

// SenseLevelEntry - scheme for senselevel
type SenseLevelEntry struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Word      string             `json:"word,omitempty" bson:"word,omitempty"`
	SenseList []SenseLevelData   `json:"senselist,omitempty" bson:"senselist,omitempty"`
	WordLevel SenseLevelData     `json:"wordlevel,omitempty" bson:"wordlevel,omitempty"`
}

// SenseLevelData - scheme for senselevel data
type SenseLevelData struct {
	Associations []string `json:"associations,omitempty" bson:"associations,omitempty"`
	Sense        []string `json:"sense,omitempty" bson:"sense,omitempty"`
}

// AffectIntensityEntry - scheme for affect intensity
type AffectIntensityEntry struct {
	ID         primitive.ObjectID    `json:"_id,omitempty" bson:"_id,omitempty"`
	Word       string                `json:"word,omitempty" bson:"word,omitempty"`
	AffectList []AffectIntensityData `json:"affectlist,omitempty" bson:"affectlist,omitempty"`
}

// AffectIntensityData - scheme for affect intensity data
type AffectIntensityData struct {
	AffectDimension string `json:"affectdimension,omitempty" bson:"affectdimension,omitempty"`
	Score           string `json:"score,omitempty" bson:"score,omitempty"`
}

// ColorEntry - scheme for color
type ColorEntry struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Word      string             `json:"word,omitempty" bson:"word,omitempty"`
	ColorList []ColorData        `json:"colorlist,omitempty" bson:"colorlist,omitempty"`
}

// ColorData - scheme for color data
type ColorData struct {
	Color      string   `json:"color,omitempty" bson:"color,omitempty"`
	Totalvotes string   `json:"totalvotes,omitempty" bson:"totalvotes,omitempty"`
	Votes      string   `json:"votes,omitempty" bson:"votes,omitempty"`
	Sense      []string `json:"sense,omitempty" bson:"sense,omitempty"`
}

// VADEntry - scheme for VAD
type VADEntry struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Word      string             `json:"word,omitempty" bson:"word,omitempty"`
	Valence   string             `json:"valence,omitempty" bson:"valence,omitempty"`
	Arousal   string             `json:"arousal,omitempty" bson:"arousal,omitempty"`
	Dominance string             `json:"dominance,omitempty" bson:"dominance,omitempty"`
}
