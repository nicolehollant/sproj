package main

// pls peep this l8r https://medium.com/@wembleyleach/how-to-use-the-official-mongodb-go-driver-9f8aff716fdb

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var client *mongo.Client

func main() {
	fmt.Println("Starting the application...")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	cancel()
	defaultURI := "mongodb://database:27017"
	db := os.Getenv("database")
	network := os.Getenv("app-network")
	mongoPort := os.Getenv("MONGOPORT")
	fmt.Println("DB HOST:")
	fmt.Println(db)
	fmt.Println("NETWORk:")
	fmt.Println(network)
	fmt.Println("MONGO PORT:")
	fmt.Println(mongoPort)
	uri := "mongodb://" + db + ":" + mongoPort
	if db == "" {
		uri = defaultURI
	}
	clientOptions := options.Client().ApplyURI(uri)
	client, _ = mongo.Connect(ctx, clientOptions)
	router := mux.NewRouter()
	// Routes below
	router.HandleFunc("/thesaurus/api/v1", GetAPIInfo).Methods("GET")
	router.HandleFunc("/thesaurus/api/v1/admin/words", CreateWord).Methods("POST")
	router.HandleFunc("/thesaurus/api/v1/admin/words", GetAllWords).Methods("GET")
	router.HandleFunc("/thesaurus/api/v1/admin/words", UpdateWord).Methods("PUT")
	router.HandleFunc("/thesaurus/api/v1/admin/words", DeleteWord).Methods("DELETE")
	router.HandleFunc("/thesaurus/api/v1/words/{word}", GetWord).Methods("GET")
	http.ListenAndServe(":12345", router)
}
