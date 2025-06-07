package dto

import (
	"db-admin/models/entities"

	"github.com/google/uuid"
)

type ConnectionCreate struct {
	ConnectionString string `json:"connection_string" binding:"required"`
	Name             string `json:"name" binding:"required"`
	Driver           string `json:"driver" binding:"required"`
}

type ConnectionUpdate struct {
	ConnectionCreate
}

type ConnectionOutput struct {
	ID               uuid.UUID `json:"id"`
	ConnectionString string    `json:"connection_string"`
	Name             string    `json:"name"`
	Driver           string    `json:"driver"`
}

func (c *ConnectionCreate) ToConnection() (*entities.Connection, error) {
	return entities.NewConnection(c.ConnectionString, c.Name, c.Driver)
}

func ToConnectionOutput(c *entities.Connection) ConnectionOutput {
	return ConnectionOutput{
		ID:               c.ID,
		ConnectionString: "********", // Mask sensitive data
		Name:             c.Name,
		Driver:           c.Driver,
	}
}
