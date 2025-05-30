package entities

import "github.com/google/uuid"

type Connection struct {
	ID               uuid.UUID `db:"id"`
	ConnectionString string    `db:"connection_string"`
	Name             string    `db:"name"`
	Driver           string    `db:"driver"`
}
