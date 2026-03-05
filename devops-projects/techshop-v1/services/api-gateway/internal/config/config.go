package config

import (
	"os"
	"strconv"
)

type Config struct {
	ProductServiceURL string
	OrderServiceURL   string
	UserServiceURL    string

	JWTSecret  string
	ServerPort string
	RateLimit  int
}

func Load() *Config {
	return &Config{
		ProductServiceURL: getEnv("PRODUCT_SERVICE_URL", "http://localhost:8080"),
		OrderServiceURL:   getEnv("ORDER_SERVICE_URL", "http://localhost:5030"),
		UserServiceURL:    getEnv("USER_SERVICE_URL", "http://localhost:5020"),

		JWTSecret:  getEnv("JWT_SECRET", "secret"),
		ServerPort: getEnv("SERVER_PORT", "8020"),
		RateLimit:  getEnvInt("RATE_LIMIT", 100),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	valueStr := os.Getenv(key)
	if valueStr == "" {
		return defaultValue
	}

	value, err := strconv.Atoi(valueStr)
	if err != nil {
		return defaultValue
	}

	return value
}
