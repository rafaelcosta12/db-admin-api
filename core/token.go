package core

import (
	"db-admin/models"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte("my_secret_key")

func GenerateToken(user models.User) (string, error) {
	claims := jwt.MapClaims{
		"sub":      user.ID,
		"iss":      "db-admin.devstacker.com",
		"iat":      time.Now().Unix(),
		"user_id":  user.ID,
		"email":    user.Email,
		"name":     user.Name,
		"is_admin": user.IsAdmin,
		"exp":      time.Now().Add(time.Hour * 72).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}

func ValidateToken(tokenString string) (models.UserToken, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return jwtSecret, nil
	})

	if err != nil {
		return models.UserToken{}, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		user := models.UserToken{
			ID:      int(claims["user_id"].(float64)),
			Email:   claims["email"].(string),
			Name:    claims["name"].(string),
			IsAdmin: claims["is_admin"].(bool),
		}
		return user, nil
	}

	return models.UserToken{}, jwt.ErrSignatureInvalid
}
