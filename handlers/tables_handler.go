package handlers

import (
	"db-admin/models"
	"db-admin/repositories"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func GetTables(c *gin.Context) {
	connectionID, err := uuid.Parse(c.Param("connection_id"))
	if err != nil {
		c.JSON(400, gin.H{"error": "Invalid connection ID"})
		return
	}

	managedTables, err := repositories.GetManagedTablesByConnection(connectionID)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to retrieve managed tables"})
		return
	}

	var schemasNames []string
	var tablesNames []string

	for _, table := range managedTables {
		schemasNames = append(schemasNames, table.SchemaName)
		tablesNames = append(tablesNames, table.TableName)
	}

	tables, err := repositories.GetTables(connectionID, schemasNames, tablesNames)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to retrieve tables"})
		return
	}

	output := make([]any, len(tables))
	for i, table := range tables {
		output[i] = models.ManagedTableOutputWithColumnOutput{
			ID:          managedTables[i].ID,
			TableOutput: table.ToOutput(),
		}
	}

	c.JSON(200, output)
}

func CreateTableRow(c *gin.Context) {
	_, err := uuid.Parse(c.Param("connection_id"))
	if err != nil {
		c.JSON(400, gin.H{"error": "Invalid connection ID"})
		return
	}

	var input map[string]interface{}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(400, gin.H{"error": "Invalid input data"})
		return
	}

	c.Status(201)
}
