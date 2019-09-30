// package app

// import (
// 	"context"
// 	"fmt"
// 	"log"
// 	"net/http"
// 	"os"
// 	"time"

// 	"github.com/gorilla/handlers"
// 	"github.com/gorilla/mux"
// 	"go.mongodb.org/mongo-driver/mongo"
// 	"go.mongodb.org/mongo-driver/mongo/options"
// )

// var client *mongo.Client

// func commonMiddleware(next http.Handler) http.Handler {
// 	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		if origin := r.Header.Get("Origin"); origin != "" {
// 			fmt.Println("askdjasd")
// 			w.Header().Set("Access-Control-Allow-Origin", origin)
// 			w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
// 			w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
// 		}
// 		w.Header().Set("Content-Type", "application/json")
// 		next.ServeHTTP(w, r)
// 	})
// }

// func main() {
// 	fmt.Println("Starting the application...")
// 	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
// 	cancel()
// 	defaultURI := "mongodb://database:27017"
// 	// defaultURI := "mongodb://67.205.167.246:27017"
// 	db := os.Getenv("database")
// 	network := os.Getenv("app-network")
// 	mongoPort := os.Getenv("MONGOPORT")
// 	fmt.Println("DB HOST:")
// 	fmt.Println(db)
// 	fmt.Println("NETWORk:")
// 	fmt.Println(network)
// 	fmt.Println("MONGO PORT:")
// 	fmt.Println(mongoPort)
// 	uri := "mongodb://" + db + ":" + mongoPort
// 	if db == "" {
// 		uri = defaultURI
// 	}
// 	clientOptions := options.Client().ApplyURI(uri)
// 	client, _ = mongo.Connect(ctx, clientOptions)
// 	router := mux.NewRouter()

// 	router.Use(commonMiddleware)
// 	// Routes below
// 	router.HandleFunc("/thesaurus/api/v1", GetAPIInfo).Methods("GET")
// 	router.HandleFunc("/thesaurus/api/v1/admin/words", CreateWord).Methods("POST")
// 	router.HandleFunc("/thesaurus/api/v1/admin/words", GetAllWords).Methods("GET")
// 	router.HandleFunc("/thesaurus/api/v1/admin/words", UpdateWord).Methods("PUT")
// 	router.HandleFunc("/thesaurus/api/v1/admin/words", DeleteWord).Methods("DELETE")
// 	router.HandleFunc("/thesaurus/api/v1/words/{word}", GetWord).Methods("GET")
// 	log.Fatal(http.ListenAndServe("0.0.0.0:3000", handlers.CORS(handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"}), handlers.AllowedMethods([]string{"GET", "POST", "PUT", "HEAD", "OPTIONS"}), handlers.AllowedOrigins([]string{"*"}))(router)))

// }

package app

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/colehollant/sproj/thesaurus/gobackend/endpoints"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// App has router and db instances
type App struct {
	Router *mux.Router
	Client *mongo.Client
}

func commonMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if origin := r.Header.Get("Origin"); origin != "" {
			w.Header().Set("Access-Control-Allow-Origin", origin)
			w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
			w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		}
		w.Header().Set("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
}

// Initialize initializes the app with predefined configuration
func (a *App) Initialize(config *config.Config) {
	uri := "mongodb://" + config.DB.Host + ":" + config.DB.Port
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	cancel()
	defaultURI := "mongodb://database:27017"
	// defaultURI := "mongodb://67.205.167.246:27017"
	if db == "" {
		uri = defaultURI
	}
	clientOptions := options.Client().ApplyURI(uri)
	a.Client, _ = mongo.Connect(ctx, clientOptions)

	a.Router = mux.NewRouter()
	a.Router.Use(commonMiddleware)
	a.setRouters()
}

// setRouters sets the all required routers
func (a *App) setRouters() {
	// Routes below
	a.Get("/thesaurus/api/v1", a.handleRequest(endpoints.GetAPIInfo))
	a.Post("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.CreateWord))
	a.Get("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.GetAllWords))
	a.Put("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.UpdateWord))
	a.Delete("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.DeleteWord))
	a.Get("/thesaurus/api/v1/words/{word}", a.handleRequest(endpoints.GetWord))
}

// Get wraps the router for GET method
func (a *App) Get(path string, f func(w http.ResponseWriter, r *http.Request)) {
	a.Router.HandleFunc(path, f).Methods("GET")
}

// Post wraps the router for POST method
func (a *App) Post(path string, f func(w http.ResponseWriter, r *http.Request)) {
	a.Router.HandleFunc(path, f).Methods("POST")
}

// Put wraps the router for PUT method
func (a *App) Put(path string, f func(w http.ResponseWriter, r *http.Request)) {
	a.Router.HandleFunc(path, f).Methods("PUT")
}

// Delete wraps the router for DELETE method
func (a *App) Delete(path string, f func(w http.ResponseWriter, r *http.Request)) {
	a.Router.HandleFunc(path, f).Methods("DELETE")
}

// Run the app on it's router
func (a *App) Run(host string) {
	// log.Fatal(http.ListenAndServe(host, a.Router))
	log.Fatal(http.ListenAndServe(host,
		handlers.CORS(handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"}),
			handlers.AllowedMethods([]string{"GET", "POST", "PUT", "HEAD", "OPTIONS"}),
			handlers.AllowedOrigins([]string{"*"}))(a.Router)))
}

type RequestHandlerFunction func(client *mongo.Client, w http.ResponseWriter, r *http.Request)

func (a *App) handleRequest(handler RequestHandlerFunction) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		handler(a.Client, w, r)
	}
}
