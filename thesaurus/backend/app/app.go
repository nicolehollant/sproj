package app

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/colehollant/sproj/thesaurus/backend/app/endpoints"
	"github.com/colehollant/sproj/thesaurus/backend/config"
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
	if config.DB.Host == "" {
		uri = defaultURI
	}
	fmt.Println("DB HOST:")
	fmt.Println(config.DB.Host)
	fmt.Println("MONGO PORT:")
	fmt.Println(config.DB.Port)
	fmt.Println("URI:")
	fmt.Println(uri)
	fmt.Println("O hi there")
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

	a.Post("/thesaurus/api/v1/admin/senselevel", a.handleRequest(endpoints.CreateSenseLevel))
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

// RequestHandlerFunction -- request handler wrapper
type RequestHandlerFunction func(client *mongo.Client, w http.ResponseWriter, r *http.Request)

func (a *App) handleRequest(handler RequestHandlerFunction) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		handler(a.Client, w, r)
	}
}
