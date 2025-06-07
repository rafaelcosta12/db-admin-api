package tables

import (
	"db-admin/models/entities"

	"github.com/google/uuid"
)

type ConnectionTable struct {
	ID               uuid.UUID `db:"id"`
	ConnectionString string    `db:"connection_string"`
	Name             string    `db:"name"`
	Driver           string    `db:"driver"`
}

func ToConnectionTable(dest *entities.Connection) ConnectionTable {
	return ConnectionTable{
		ID:               dest.ID,
		ConnectionString: dest.ConnectionString,
		Name:             dest.Name,
		Driver:           dest.Driver,
	}
}

func FromConnectionTable(src *ConnectionTable) *entities.Connection {
	return &entities.Connection{
		Entity:           entities.Entity{ID: src.ID},
		ConnectionString: src.ConnectionString,
		Name:             src.Name,
		Driver:           src.Driver,
	}
}
