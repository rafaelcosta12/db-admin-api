package handlers

import (
	"db-admin/models/dto"
	"db-admin/repositories"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetManagedTables(c *gin.Context) {
	tables, err := repositories.GetManagedTables()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve managed tables"})
		return
	}

	output := make([]any, len(tables))
	for i, table := range tables {
		output[i] = dto.ToManagedTableOutput(&table)
	}

	c.JSON(http.StatusOK, output)
}

func CreateManagedTable(c *gin.Context) {
	var input dto.ManagedTableCreate
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input data"})
		return
	}

	createdTable, err := repositories.CreateManagedTable(input.ToManagedTable())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create managed table"})
		return
	}

	c.JSON(http.StatusCreated, dto.ToManagedTableOutput(&createdTable))
}
