package handlers

import (
	"database/sql"
	"db-admin/models"
	"db-admin/repositories"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func searchParams(c *gin.Context) models.UserSearch {
	search := models.UserSearch{
		Limit:    10,
		Offset:   0,
		Order:    models.Asc,
		Text:     "%",
		OrderBy:  models.CreatedAtOrderBy,
		IsActive: nil,
		IsAdmin:  nil,
	}

	search.Limit, _ = strconv.Atoi(c.Query("limit"))
	search.Offset, _ = strconv.Atoi(c.Query("offset"))

	orderBy := c.Query("order_by")
	if orderBy == "" || orderBy == "created_at" {
		search.OrderBy = models.CreatedAtOrderBy
	} else if orderBy == "email" {
		search.OrderBy = models.EmailOrderBy
	} else if orderBy == "name" {
		search.OrderBy = models.NameOrderBy
	} else if orderBy == "is_admin" {
		search.OrderBy = models.IsAdminOrderBy
	} else if orderBy == "is_active" {
		search.OrderBy = models.IsActiveOrderBy
	} else if orderBy == "updated_at" {
		search.OrderBy = models.UpdatedAtOrderBy
	}

	order := c.Query("order")
	if order == "" || order == "asc" {
		search.Order = models.Asc
	} else if order == "desc" {
		search.Order = models.Desc
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

	c.JSON(http.StatusOK, models.Pagination{
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
	var input models.UserCreate

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

	var input models.UserUpdate
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

	user, err := repositories.GetUserByID(u.(models.UserToken).ID)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Invalid user data"})
		return
	}

	c.JSON(http.StatusOK, user.ToOutput())
}
