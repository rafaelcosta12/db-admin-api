package repositories

import (
	"db-admin/core"
	"db-admin/models"

	"github.com/google/uuid"
)

func GetConnectionByID(id uuid.UUID) (models.Connection, error) {
	return core.GetConnectionByID(id)
}

func CreateConnection(connection models.Connection) (models.Connection, error) {
	return core.CreateConnection(connection)
}

func UpdateConnection(id uuid.UUID, connection models.Connection) (models.Connection, error) {
	return core.UpdateConnection(id, connection)
}

func DeleteConnection(id uuid.UUID) error {
	return core.DeleteConnection(id)
}

func GetAllConnections() ([]models.Connection, error) {
	connections := []models.Connection{}
	err := core.AppDB.Select(&connections, "SELECT id, driver, connection_string, name FROM connections")
	if err != nil {
		return nil, err
	}
	return connections, nil
}
