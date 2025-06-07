package core

import (
	"db-admin/models/entities"
	"net/http"

	"github.com/gin-gonic/gin"
)

var TokenPrefix = "Bearer"

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// check if is a request to the auth endpoint
		if c.Request.URL.Path == "/auth/login" || c.Request.Method == "OPTIONS" {
			c.Next()
			return
		}

		token := c.Request.Header.Get("Authorization")
		if token == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header is required"})
			c.Abort()
			return
		}

		if len(token) > 7 && token[:7] == (TokenPrefix+" ") {
			token = token[7:]
		}

		user, err := ValidateToken(token)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			c.Abort()
			return
		}

		c.Set("user", user)
		c.Next()
	}
}

func ShouldBeAdminOr403() gin.HandlerFunc {
	return func(c *gin.Context) {
		user, exists := c.Get("user")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found"})
			c.Abort()
			return
		}

		if !user.(entities.UserToken).IsAdmin {
			c.JSON(http.StatusForbidden, gin.H{"error": "You do not have permission to access this resource"})
			c.Abort()
			return
		}

		c.Next()
	}
}
