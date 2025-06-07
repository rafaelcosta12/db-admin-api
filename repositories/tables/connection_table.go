package tables

import (
	"db-admin/models/entities"

	"github.com/google/uuid"
)

type ConnectionTable struct {
	ID               uuid.UUID `db:"id"`
	ConnectionString string    `db:"connection_string"`
	Name             string    `db:"name"`
}

func ToConnectionTable(dest *entities.Connection) ConnectionTable {
	return ConnectionTable{
		ID:               dest.ID,
		ConnectionString: dest.ConnectionString.String(),
		Name:             dest.Name,
	}
}

func FromConnectionTable(src *ConnectionTable) (*entities.Connection, error) {
	return entities.NewConnection(src.ConnectionString, src.Name)
}
