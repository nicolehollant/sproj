package main

import (
	"github.com/colehollant/sproj/thesaurus/backend/app"
	"github.com/colehollant/sproj/thesaurus/backend/config"
)

func main() {
	// "github.com/colehollant/sproj/thesaurus/backend/app"
	// "github.com/colehollant/sproj/thesaurus/backend/config"
	config := config.GetConfig()

	app := &app.App{}
	app.Initialize(config)
	app.Run(":3000")
}
