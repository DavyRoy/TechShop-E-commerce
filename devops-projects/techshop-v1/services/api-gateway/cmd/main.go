package main

import (
	"os"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"github.com/techshop/api-gateway/internal/config"
	"github.com/techshop/api-gateway/internal/routes"
)

func main() {
	// Logger
	log := logrus.New()
	log.SetFormatter(&logrus.JSONFormatter{})
	log.SetOutput(os.Stdout)
	// Load config
	cfg := config.Load()
	log.WithFields(logrus.Fields{
		"port": cfg.ServerPort,
	}).Info("Starting API Gateway")
	// Gin mode
	gin.SetMode(gin.ReleaseMode)
	// Router
	r := routes.SetupRouter(cfg, log)
	// Start server
	if err := r.Run(":" + cfg.ServerPort); err != nil {
		log.WithError(err).Fatal("Failed to start server")
	}
}
