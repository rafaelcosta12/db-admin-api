package handlers

import (
	"db-admin/core"
	"db-admin/models/dto"
	"db-admin/repositories"
	"net/http"

	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

func Login(c *gin.Context) {
	var input dto.UserLogin
	err := c.ShouldBindJSON(&input)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := repositories.GetUserByEmail(input.Email)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
		return
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(input.Password))
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
		return
	}

	token, err := core.GenerateToken(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not generate token"})
		return
	}

	c.JSON(http.StatusOK, dto.LoginResponse{Token: token, Prefix: core.TokenPrefix})
}

func Logout(c *gin.Context) {
	// In a real application, you would invalidate the token here.
	// For this example, we will just return a success message.
	c.JSON(http.StatusOK, gin.H{"message": "Logged out successfully"})
}
