package handlers

import (
	"github.com/gin-gonic/gin"
)

func GetSchemas(c *gin.Context) {
	// connectionId, err := uuid.Parse(c.Param("id"))
	// if err != nil {
	// 	c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid connection ID"})
	// 	return
	// }

	// schemas, err := repositories.GetSchemas(connectionId)
	// if err != nil {
	// 	c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve tables"})
	// 	return
	// }

	// output := make([]any, len(schemas))
	// for i, schema := range schemas {
	// 	output[i] = schema.ToOutput()
	// }

	// c.JSON(http.StatusOK, output)
}
