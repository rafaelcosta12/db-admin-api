//go:build integration

package handlers

import (
	"bytes"
	"db-admin/core"
	"db-admin/models/configurations"
	"db-admin/repositories"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"strconv"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func setupRouter() *gin.Engine {
	gin.SetMode(gin.TestMode)
	r := gin.Default()
	r.POST("/users", CreateUser)
	r.PUT("/users/:id", UpdateUser)
	r.GET("/users/me", GetMe)
	return r
}

func TestMain(m *testing.M) {
	// Setup test DB connection if needed
	// core.DB = ... (set up test DB here)
	core.ConfigureAppDB()
	code := m.Run()
	// Optionally clean up DB
	os.Exit(code)
}

func cleanupUserByEmail(email string) {
	core.AppDB.Exec("DELETE FROM users WHERE email = $1", email)
}

func createDummyUser() configurations.User {
	email := "integration_test_dup@example.com"
	cleanupUserByEmail(email)
	user := configurations.UserCreate{
		Email:    email,
		Password: "password123",
		Name:     "Dup User",
	}
	u, _ := user.ToUser()
	u, _ = repositories.CreateUser(u)
	return u
}

func TestCreateUser_Success(t *testing.T) {
	router := setupRouter()
	email := "integration_test_user@example.com"
	cleanupUserByEmail(email)
	defer cleanupUserByEmail(email)

	input := configurations.UserCreate{
		Email:    email,
		Password: "password123",
		Name:     "Test User",
	}
	body, _ := json.Marshal(input)
	req, _ := http.NewRequest("POST", "/users", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusCreated, w.Code)
	var resp map[string]any
	err := json.Unmarshal(w.Body.Bytes(), &resp)
	assert.NoError(t, err)
	assert.Equal(t, email, resp["email"])
}

func TestCreateUser_Duplicate(t *testing.T) {
	router := setupRouter()
	user := createDummyUser()
	defer cleanupUserByEmail(user.Email)

	body, _ := json.Marshal(user)
	req, _ := http.NewRequest("POST", "/users", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusConflict, w.Code)
	var resp map[string]any
	_ = json.Unmarshal(w.Body.Bytes(), &resp)
	assert.Contains(t, resp["error"], "User already exists")
}

func TestUpdateUser_Success(t *testing.T) {
	router := setupRouter()
	u := createDummyUser()
	defer cleanupUserByEmail(u.Email)

	update := configurations.UserUpdate{
		Name:       "Dup User",
		IsAdmin:    false,
		IsActive:   true,
		ProfileImg: nil,
	}

	body, _ := json.Marshal(update)
	req, _ := http.NewRequest("PUT", "/users/"+strconv.Itoa(u.ID), bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	var resp map[string]any
	_ = json.Unmarshal(w.Body.Bytes(), &resp)
	assert.Equal(t, resp["name"], update.Name)
}
