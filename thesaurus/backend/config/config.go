package config

import "os"

type Config struct {
	DB *DBConfig
}

type DBConfig struct {
	Host     string
	Port     string
	Username string
	Password string
}

func GetConfig() *Config {
	return &Config{
		DB: &DBConfig{
			Host:     os.Getenv("DBHOST"),
			Port:     os.Getenv("MONGOPORT"),
			Username: os.Getenv("MONGO_USERNAME"),
			Password: os.Getenv("MONGO_PASSWORD"),
		},
	}
}
