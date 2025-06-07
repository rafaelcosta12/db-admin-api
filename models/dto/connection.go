package dto

import (
	"db-admin/models/entities"

	"github.com/google/uuid"
)

type ConnectionCreate struct {
	ConnectionString string `json:"connection_string" binding:"required"`
	Name             string `json:"name" binding:"required"`
}

type ConnectionUpdate struct {
	ConnectionCreate
}

type ConnectionOutput struct {
	ID               uuid.UUID `json:"id"`
	ConnectionString string    `json:"connection_string"`
	Name             string    `json:"name"`
}

func (c *ConnectionCreate) ToConnection() (*entities.Connection, error) {
	return entities.NewConnection(c.ConnectionString, c.Name)
}

func ToConnectionOutput(c *entities.Connection) ConnectionOutput {
	return ConnectionOutput{
		ID:               c.ID,
		ConnectionString: c.ConnectionString.String(), // Mask sensitive data
		Name:             c.Name,
	}
}
