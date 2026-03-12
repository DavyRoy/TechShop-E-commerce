package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"github.com/techshop/api-gateway/internal/config"
	"github.com/techshop/api-gateway/internal/middleware"
	"github.com/techshop/api-gateway/internal/proxy"
)

func SetupRouter(cfg *config.Config, logger *logrus.Logger) *gin.Engine {
	r := gin.New()
	r.Use(gin.Recovery())
	r.Use(middleware.LoggingMiddleware(logger))
	r.Use(middleware.RateLimitMiddleware())

	p := proxy.New(cfg.ProductServiceURL, cfg.OrderServiceURL, cfg.UserServiceURL)

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "api-gateway"})
	})

	// Публичные routes
	r.Any("/api/auth/*path", p.UserService)
	r.GET("/api/products", p.ProductService)
	r.GET("/api/products/:id", p.ProductService)

	// Защищённые routes
	protected := r.Group("/api")
	protected.Use(middleware.AuthMiddleware(cfg.JWTSecret))
	{
		protected.POST("/products", p.ProductService)
		protected.PUT("/products/:id", p.ProductService)
		protected.DELETE("/products/:id", p.ProductService)
		protected.Any("/orders", p.OrderService)
		protected.Any("/orders/*path", p.OrderService)
		protected.Any("/users/*path", p.UserService)
	}

	return r
}
