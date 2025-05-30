package handlers

import (
	"database/sql"
	"db-admin/models/auth"
	"db-admin/models/configurations"
	"db-admin/repositories"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func searchParams(c *gin.Context) configurations.UserSearch {
	search := configurations.UserSearch{
		Limit:    10,
		Offset:   0,
		Order:    configurations.Asc,
		Text:     "%",
		OrderBy:  configurations.CreatedAtOrderBy,
		IsActive: nil,
		IsAdmin:  nil,
	}

	search.Limit, _ = strconv.Atoi(c.Query("limit"))
	search.Offset, _ = strconv.Atoi(c.Query("offset"))

	orderBy := c.Query("order_by")
	if orderBy == "" || orderBy == "created_at" {
		search.OrderBy = configurations.CreatedAtOrderBy
	} else if orderBy == "email" {
		search.OrderBy = configurations.EmailOrderBy
	} else if orderBy == "name" {
		search.OrderBy = configurations.NameOrderBy
	} else if orderBy == "is_admin" {
		search.OrderBy = configurations.IsAdminOrderBy
	} else if orderBy == "is_active" {
		search.OrderBy = configurations.IsActiveOrderBy
	} else if orderBy == "updated_at" {
		search.OrderBy = configurations.UpdatedAtOrderBy
	}

	order := c.Query("order")
	if order == "" || order == "asc" {
		search.Order = configurations.Asc
	} else if order == "desc" {
		search.Order = configurations.Desc
	}

	text := c.Query("text")
	if text == "" {
		search.Text = "%"
	} else {
		search.Text = "%" + text + "%"
	}

	isActive := c.Query("is_active")
	if isActive != "" {
		search.IsActive = new(bool)

		if isActive == "true" {
			*search.IsActive = true
		} else if isActive == "false" {
			*search.IsActive = false
		}
	}

	isAdmin := c.Query("is_admin")
	if isAdmin == "true" {
		search.IsAdmin = new(bool)
		*search.IsAdmin = true
	} else if isAdmin == "false" {
		search.IsAdmin = new(bool)
		*search.IsAdmin = false
	}

	return search
}

func GetUsers(c *gin.Context) {
	searchParams := searchParams(c)
	users, err := repositories.GetUsers(searchParams)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	items := make([]any, len(users))
	for i, user := range users {
		items[i] = user.ToOutput()
	}

	c.JSON(http.StatusOK, configurations.Pagination{
		Total: len(items),
		Page:  1,
		Items: items,
	})
}

func GetUserByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	user, err := repositories.GetUserByID(id)
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		}
		return
	}
	c.JSON(http.StatusOK, user.ToOutput())
}

func validateEmailExistence(email string) (bool, error) {
	_, err := repositories.GetUserByEmail(email)
	return err == sql.ErrNoRows, err
}

func CreateUser(c *gin.Context) {
	var input configurations.UserCreate

	err := c.ShouldBindJSON(&input)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if isValid, err := validateEmailExistence(input.Email); !isValid {
		if err == nil {
			c.JSON(http.StatusConflict, gin.H{"error": "User already exists"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	user, err := input.ToUser()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	user, err = repositories.CreateUser(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, user.ToOutput())
}

func UpdateUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	var input configurations.UserUpdate
	err = c.ShouldBindJSON(&input)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := repositories.GetUserByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		return
	}

	user.Update(input)
	user, err = repositories.UpdateUser(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, user.ToOutput())
}

func DeleteUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	err = repositories.DeleteUser(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

func GetMe(c *gin.Context) {
	u, exists := c.Get("user")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Unauthorized"})
		return
	}

	user, err := repositories.GetUserByID(u.(auth.UserToken).ID)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Invalid user data"})
		return
	}

	c.JSON(http.StatusOK, user.ToOutput())
}
