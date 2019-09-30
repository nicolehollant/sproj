package main

// pls peep this l8r https://medium.com/@wembleyleach/how-to-use-the-official-mongodb-go-driver-9f8aff716fdb

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
	"endpoints"
	"structs"

	"github.com/colehollant/sproj/thesaurus/gobackend/structs"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var client *mongo.Client

func commonMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if origin := r.Header.Get("Origin"); origin != "" {
			fmt.Println("askdjasd")
			w.Header().Set("Access-Control-Allow-Origin", origin)
			w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
			w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		}
		w.Header().Set("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

func main() {
	fmt.Println("Starting the application...")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	cancel()
	defaultURI := "mongodb://database:27017"
	// defaultURI := "mongodb://67.205.167.246:27017"
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

	router.Use(commonMiddleware)
	// Routes below
	router.HandleFunc("/thesaurus/api/v1", GetAPIInfo).Methods("GET")
	router.HandleFunc("/thesaurus/api/v1/admin/words", CreateWord).Methods("POST")
	router.HandleFunc("/thesaurus/api/v1/admin/words", GetAllWords).Methods("GET")
	router.HandleFunc("/thesaurus/api/v1/admin/words", UpdateWord).Methods("PUT")
	router.HandleFunc("/thesaurus/api/v1/admin/words", DeleteWord).Methods("DELETE")
	router.HandleFunc("/thesaurus/api/v1/words/{word}", GetWord).Methods("GET")
	log.Fatal(http.ListenAndServe("0.0.0.0:3000", handlers.CORS(handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"}), handlers.AllowedMethods([]string{"GET", "POST", "PUT", "HEAD", "OPTIONS"}), handlers.AllowedOrigins([]string{"*"}))(router)))

}
