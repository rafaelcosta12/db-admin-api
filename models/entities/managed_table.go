package entities

import (
	"github.com/google/uuid"
)

type ManagedTable struct {
	ID           uuid.UUID `db:"id" json:"id"`
	ConnectionID uuid.UUID `db:"connection_id" json:"connection_id"`
	TableName    string    `db:"table_name" json:"table_name"`
	SchemaName   string    `db:"schema_name" json:"schema_name"`
}
