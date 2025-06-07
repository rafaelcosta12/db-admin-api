package handlers

import (
	"db-admin/infrastructure"
	"db-admin/models/dto"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func CreateConnection(c *gin.Context) {
	// Bind the incoming JSON to the ConnectionCreate DTO
	var input dto.ConnectionCreate
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Convert the DTO to a Connection entity
	connection, err := input.ToConnection()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	ConnectionRepository := infrastructure.ConnectionRepository{}

	// Save the connection using the repository
	err = ConnectionRepository.Save(connection)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Return the created connection as a response
	c.JSON(http.StatusCreated, dto.ToConnectionOutput(connection))
}

func GetConnections(c *gin.Context) {
	ConnectionRepository := infrastructure.ConnectionRepository{}

	connections, err := ConnectionRepository.GetAll()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve connections"})
		return
	}

	var output []any = make([]any, len(*connections))
	for i, conn := range *connections {
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

	ConnectionRepository := infrastructure.ConnectionRepository{}

	// Retrieve the connection by ID
	connection, err := ConnectionRepository.GetById(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Connection not found"})
		return
	}

	// Delete the connection using the repository
	err = ConnectionRepository.Delete(connection)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete connection"})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}
