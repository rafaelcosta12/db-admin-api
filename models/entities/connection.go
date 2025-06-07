package entities

import (
	"fmt"

	"github.com/google/uuid"
)

type Connection struct {
	Entity
	ConnectionString string
	Name             string
	Driver           string
}

func NewConnection(connectionString, name, driver string) (*Connection, error) {
	if connectionString == "" || name == "" || driver == "" {
		return nil, fmt.Errorf("connection string, name, and driver must not be empty")
	}

	return &Connection{
		Entity: Entity{
			ID: uuid.New(),
		},
		ConnectionString: connectionString,
		Name:             name,
		Driver:           driver,
	}, nil
}
