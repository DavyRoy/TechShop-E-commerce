package config

import "os"

type Config struct {
	MongoURI   string
	MongoDB    string
	ServerPort string
	LogLevel   string
}

func Load() *Config {
	return &Config{
		MongoURI:   getEnv("MONGODB_URI", "mongodb://localhost:27017"),
		MongoDB:    getEnv("MONGODB_DB", "techshop"),
		ServerPort: getEnv("SERVER_PORT", "8080"),
		LogLevel:   getEnv("LOG_LEVEL", "info"),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
