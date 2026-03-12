package middleware

import (
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func AuthMiddleware(secret string) gin.HandlerFunc {
	return func(c *gin.Context) {

		authHeader := c.GetHeader("Authorization")

		if authHeader == "" || !strings.HasPrefix(authHeader, "Bearer ") {
			c.JSON(401, gin.H{
				"error": gin.H{
					"code":   "UNAUTHORIZED",
					"status": 401,
				},
			})
			c.Abort()
			return
		}

		tokenStr := strings.TrimPrefix(authHeader, "Bearer ")

		token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {

			// проверяем алгоритм подписи
			if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, jwt.ErrTokenSignatureInvalid
			}

			return []byte(secret), nil
		})

		if err != nil || !token.Valid {
			c.JSON(401, gin.H{
				"error": gin.H{
					"code":   "INVALID_TOKEN",
					"status": 401,
				},
			})
			c.Abort()
			return
		}

		c.Next()
	}
}
