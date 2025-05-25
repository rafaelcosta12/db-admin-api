package repositories

import (
	"db-admin/core"
	"db-admin/models"

	"github.com/google/uuid"
)

func GetSchemas(connectionID uuid.UUID) ([]models.Schema, error) {
	var schemas []models.Schema
	conn, err := core.GetDB(connectionID)
	if err != nil {
		return nil, err
	}

	err = conn.Select(&schemas, "SELECT table_schema FROM information_schema.tables")
	if err != nil {
		return nil, err
	}

	return schemas, nil
}
