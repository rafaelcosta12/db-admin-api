package connection

import (
	"db-admin/models/entities/vo"
	"fmt"

	"github.com/google/uuid"
)

type Connection struct {
	ID               uuid.UUID
	ConnectionString vo.ConnectionString
	Name             string
}

func NewConnection(connectionString, name string) (*Connection, error) {
	if connectionString == "" || name == "" {
		return nil, fmt.Errorf("connection string and name must not be empty")
	}

	connStrVo, err := vo.NewConnectionString(connectionString)
	if err != nil {
		return nil, fmt.Errorf("invalid connection string: %w", err)
	}

	return &Connection{
		ID:               uuid.New(),
		ConnectionString: connStrVo,
		Name:             name,
	}, nil
}
