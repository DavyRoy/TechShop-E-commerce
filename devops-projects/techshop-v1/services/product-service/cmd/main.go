package cmd

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/sirupsen/logrus"
	"github.com/techshop/product-service/internal/config"
	"github.com/techshop/product-service/internal/repository"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

func main() {
	log := logrus.New()
	log.SetFormatter(&logrus.JSONFormatter{})

	cfg := config.Load()
	log.WithField("port", cfg.ServerPort).Info("Starting Product Service")

	// Подключение к MongoDB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(options.Client().ApplyURI(cfg.MongoURI))
	if err != nil {
		log.WithError(err).Fatal("Failed to connect to MongoDB")
	}
	defer client.Disconnect(ctx)

	if err := client.Ping(ctx, nil); err != nil {
		log.WithError(err).Fatal("MongoDB ping failed")
	}
	log.Info("Connected to MongoDB")

	db := client.Database(cfg.MongoDB)
	_ = repository.NewProductRepository(db)
	log.Info("Repository initialized")

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	log.WithField("port", cfg.ServerPort).Info("Server is ready")
	<-quit

	log.Info("Shutting down gracefully...")
	fmt.Println("Done")
}
