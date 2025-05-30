package handlers

import (
	"database/sql"
	"db-admin/models/dto"
	"db-admin/repositories"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func searchParams(c *gin.Context) dto.UserSearch {
	search := dto.UserSearch{
		Limit:    10,
		Offset:   0,
		Order:    dto.Asc,
		Text:     "%",
		OrderBy:  dto.CreatedAtOrderBy,
		IsActive: nil,
		IsAdmin:  nil,
	}

	search.Limit, _ = strconv.Atoi(c.Query("limit"))
	search.Offset, _ = strconv.Atoi(c.Query("offset"))

	orderBy := c.Query("order_by")
	if orderBy == "" || orderBy == "created_at" {
		search.OrderBy = dto.CreatedAtOrderBy
	} else if orderBy == "email" {
		search.OrderBy = dto.EmailOrderBy
	} else if orderBy == "name" {
		search.OrderBy = dto.NameOrderBy
	} else if orderBy == "is_admin" {
		search.OrderBy = dto.IsAdminOrderBy
	} else if orderBy == "is_active" {
		search.OrderBy = dto.IsActiveOrderBy
	} else if orderBy == "updated_at" {
		search.OrderBy = dto.UpdatedAtOrderBy
	}

	order := c.Query("order")
	if order == "" || order == "asc" {
		search.Order = dto.Asc
	} else if order == "desc" {
		search.Order = dto.Desc
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
		items[i] = dto.ToUserOutput(&user)
	}

	c.JSON(http.StatusOK, dto.Pagination{
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
	c.JSON(http.StatusOK, dto.ToUserOutput(&user))
}

func validateEmailExistence(email string) (bool, error) {
	_, err := repositories.GetUserByEmail(email)
	return err == sql.ErrNoRows, err
}

func CreateUser(c *gin.Context) {
	var input dto.UserCreate

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

	c.JSON(http.StatusCreated, dto.ToUserOutput(&user))
}

func UpdateUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	var input dto.UserUpdate
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

	dto.UpdateUser(&user, input)
	user, err = repositories.UpdateUser(user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, dto.ToUserOutput(&user))
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

	user, err := repositories.GetUserByID(u.(dto.UserToken).ID)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Invalid user data"})
		return
	}

	c.JSON(http.StatusOK, dto.ToUserOutput(&user))
}
