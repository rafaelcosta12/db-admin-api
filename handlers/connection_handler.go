package handlers

import (
	"db-admin/models/dto"
	"db-admin/repositories"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func CreateConnection(c *gin.Context) {
	var connection dto.ConnectionCreate
	if err := c.ShouldBindJSON(&connection); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	conn, err := repositories.CreateConnection(connection.ToConnection())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create connection"})
		return
	}

	c.JSON(http.StatusCreated, dto.ToConnectionOutput(conn))
}

func GetConnections(c *gin.Context) {
	connections, err := repositories.GetAllConnections()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve connections"})
		return
	}

	var output []any = make([]any, len(connections))
	for i, conn := range connections {
		output[i] = dto.ToConnectionOutput(conn)
	}

	c.JSON(http.StatusOK, output)
}

func RemoveConnection(c *gin.Context) {
	id, err := uuid.Parse(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid connection ID"})
		return
	}

	err = repositories.DeleteConnection(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete connection"})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}
