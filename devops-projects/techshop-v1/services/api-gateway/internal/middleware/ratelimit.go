package middleware

import (
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/time/rate"
)

var limiters = make(map[string]*rate.Limiter)

func RateLimitMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		ip := c.ClientIP()
		limiter, exists := limiters[ip]
		if !exists {
			limiter = rate.NewLimiter(rate.Every(time.Minute/100), 100)
			limiters[ip] = limiter
		}

		if !limiter.Allow() {
			c.JSON(429, gin.H{"error": gin.H{"code": "RATE_LIMIT_EXCEEDED", "status": 429}})
			c.Abort()
			return
		}
		c.Next()
	}
}
