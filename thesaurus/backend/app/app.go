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
	localEnv := true
	localEnv = false
	uri := "mongodb://" + config.DB.Username + ":" + config.DB.Password + "@" + config.DB.Host + ":" + config.DB.Port
	defaultURI := "mongodb://" + config.DB.Username + ":" + config.DB.Password + "@" + "localhost:27017"
	if config.DB.Host == "" || localEnv == true {
		uri = defaultURI
	}
	fmt.Printf("HOST: %s, PORT: %s, URI: %s\n", config.DB.Host, config.DB.Port, uri)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	cancel()

	client, err := mongo.NewClient(options.Client().ApplyURI(uri))
	err = client.Connect(ctx)
	if err != nil {
		fmt.Printf("Failed to connect to mongo %s\n", err)
		return
	}
	a.Client = client
	a.Router = mux.NewRouter()
	a.Router.Use(commonMiddleware)
	a.setRouters()
}

// setRouters sets the all required routers
func (a *App) setRouters() {
	// General Routes
	a.Get("/thesaurus/api/v1", a.handleRequest(endpoints.GetAPIInfo))
	// Standard Thesaurus -- Admin
	a.Post("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.CreateWord))
	a.Get("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.GetAllWords))
	a.Put("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.UpdateWord))
	a.Delete("/thesaurus/api/v1/admin/words", a.handleRequest(endpoints.DeleteWord))
	// Standard Thesaurus -- Basic
	a.Get("/thesaurus/api/v1/words/{word}", a.handleRequest(endpoints.GetWord))
	// SenseLevel Lexicon -- Admin
	a.Get("/thesaurus/api/v1/admin/senselevel", a.handleRequest(endpoints.GetAllSenseLevels))
	a.Post("/thesaurus/api/v1/admin/senselevel", a.handleRequest(endpoints.CreateSenseLevel))
	a.Put("/thesaurus/api/v1/admin/senselevel", a.handleRequest(endpoints.UpdateSenseLevel))
	a.Delete("/thesaurus/api/v1/admin/senselevel", a.handleRequest(endpoints.DeleteSenseLevel))
	// SenseLevel Lexicon -- Basic
	a.Get("/thesaurus/api/v1/senselevel/{word}", a.handleRequest(endpoints.GetSenseLevel))
	// AffectIntensity Lexicon -- Admin
	a.Get("/thesaurus/api/v1/admin/affectintensity", a.handleRequest(endpoints.GetAllAffectIntensitys))
	a.Post("/thesaurus/api/v1/admin/affectintensity", a.handleRequest(endpoints.CreateAffectIntensity))
	a.Put("/thesaurus/api/v1/admin/affectintensity", a.handleRequest(endpoints.UpdateAffectIntensity))
	a.Delete("/thesaurus/api/v1/admin/affectintensity", a.handleRequest(endpoints.DeleteAffectIntensity))
	// AffectIntensity Lexicon -- Basic
	a.Get("/thesaurus/api/v1/affectintensity/{word}", a.handleRequest(endpoints.GetAffectIntensity))
	// Color Lexicon -- Admin
	a.Get("/thesaurus/api/v1/admin/color", a.handleRequest(endpoints.GetAllColors))
	a.Post("/thesaurus/api/v1/admin/color", a.handleRequest(endpoints.CreateColor))
	a.Put("/thesaurus/api/v1/admin/color", a.handleRequest(endpoints.UpdateColor))
	a.Delete("/thesaurus/api/v1/admin/color", a.handleRequest(endpoints.DeleteColor))
	// Color Lexicon -- Basic
	a.Get("/thesaurus/api/v1/color/{word}", a.handleRequest(endpoints.GetColor))
	// VAD Lexicon -- Admin
	a.Get("/thesaurus/api/v1/admin/vad", a.handleRequest(endpoints.GetAllVADs))
	a.Post("/thesaurus/api/v1/admin/vad", a.handleRequest(endpoints.CreateVAD))
	a.Put("/thesaurus/api/v1/admin/vad", a.handleRequest(endpoints.UpdateVAD))
	a.Delete("/thesaurus/api/v1/admin/vad", a.handleRequest(endpoints.DeleteVAD))
	// VAD Lexicon -- Basic
	a.Get("/thesaurus/api/v1/vad/{word}", a.handleRequest(endpoints.GetVAD))
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
