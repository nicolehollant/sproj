module github.com/colehollant/sproj/thesaurus/backend/app

go 1.12

replace github.com/colehollant/sproj/thesaurus/backend/app/endpoints => /Users/colehollant/Projects/sproj/thesaurus/backend/app/endpoints
replace github.com/colehollant/sproj/thesaurus/backend/config => /Users/colehollant/Projects/sproj/thesaurus/backend/config

require (
	github.com/colehollant/sproj/thesaurus/backend/app/endpoints v0.0.0-20190930182355-6aa5a7a83987
	github.com/colehollant/sproj/thesaurus/backend/config v0.0.0-20190930182355-6aa5a7a83987
	github.com/gorilla/handlers v1.4.2
	github.com/gorilla/mux v1.7.3
	go.mongodb.org/mongo-driver v1.1.1
)
