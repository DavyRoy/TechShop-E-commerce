package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"github.com/techshop/product-service/internal/config"
	"github.com/techshop/product-service/internal/handlers"
	"github.com/techshop/product-service/internal/repository"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

func main() {
	log := logrus.New()
	log.SetFormatter(&logrus.JSONFormatter{})

	cfg := config.Load()
	log.WithField("port", cfg.ServerPort).Info("Starting Product Service")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(options.Client().ApplyURI(cfg.MongoURI))
	if err != nil {
		log.WithError(err).Fatal("MongoDB connection failed")
	}

	if err := client.Ping(ctx, nil); err != nil {
		log.WithError(err).Fatal("MongoDB ping failed")
	}
	log.Info("Connected to MongoDB")

	db := client.Database(cfg.MongoDB)
	productRepo := repository.NewProductRepository(db)
	productHandler := handlers.NewProductHandler(productRepo, log)

	r := gin.New()
	r.Use(gin.Logger())

	r.GET("/health", productHandler.HealthCheck)
	r.POST("/products", productHandler.CreateProduct)
	r.GET("/products", productHandler.ListProducts)
	r.GET("/products/:id", productHandler.GetProduct)
	r.PUT("/products/:id", productHandler.UpdateProduct)
	r.DELETE("/products/:id", productHandler.DeleteProduct)

	srv := &http.Server{
		Addr:    ":" + cfg.ServerPort,
		Handler: r,
	}

	go func() {
		log.WithField("port", cfg.ServerPort).Info("HTTP server started")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.WithError(err).Fatal("Server failed")
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info("Shutting down gracefully...")
	ctxShut, cancelShut := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancelShut()

	srv.Shutdown(ctxShut)
	client.Disconnect(ctxShut)
	log.Info("Server stopped")
}
