package dto

import (
	"db-admin/models/entities/connection"

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

func (c *ConnectionCreate) ToConnection() (*connection.Connection, error) {
	return connection.NewConnection(c.ConnectionString, c.Name)
}

func ToConnectionOutput(c *connection.Connection) ConnectionOutput {
	return ConnectionOutput{
		ID:               c.ID,
		ConnectionString: c.ConnectionString.String(), // Mask sensitive data
		Name:             c.Name,
	}
}
