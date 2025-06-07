package tables

import (
	"db-admin/models/entities/connection"

	"github.com/google/uuid"
)

type ConnectionTable struct {
	ID               uuid.UUID `db:"id"`
	ConnectionString string    `db:"connection_string"`
	Name             string    `db:"name"`
}

func ToConnectionTable(dest *connection.Connection) ConnectionTable {
	return ConnectionTable{
		ID:               dest.ID,
		ConnectionString: dest.ConnectionString.String(),
		Name:             dest.Name,
	}
}

func FromConnectionTable(src *ConnectionTable) (*connection.Connection, error) {
	return connection.NewConnection(src.ConnectionString, src.Name)
}
