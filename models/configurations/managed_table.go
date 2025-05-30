package configurations

import (
	"db-admin/models/database"

	"github.com/google/uuid"
)

type ManagedTable struct {
	ID           uuid.UUID `db:"id" json:"id"`
	ConnectionID uuid.UUID `db:"connection_id" json:"connection_id"`
	TableName    string    `db:"table_name" json:"table_name"`
	SchemaName   string    `db:"schema_name" json:"schema_name"`
}

type ManagedTableOutput struct {
	ID           uuid.UUID `json:"id"`
	ConnectionID uuid.UUID `json:"connection_id"`
	TableName    string    `json:"table_name"`
	SchemaName   string    `json:"schema_name"`
}

type ManagedTableOutputWithColumnOutput struct {
	ID uuid.UUID `json:"id"`
	database.TableOutput
}

type ManagedTableCreate struct {
	ConnectionID uuid.UUID `json:"connection_id" binding:"required"`
	TableName    string    `json:"table_name" binding:"required"`
	SchemaName   string    `json:"schema_name" binding:"required"`
}

func (mt *ManagedTableCreate) ToManagedTable() ManagedTable {
	return ManagedTable{
		ID:           uuid.New(),
		ConnectionID: mt.ConnectionID,
		TableName:    mt.TableName,
		SchemaName:   mt.SchemaName,
	}
}

func (mt *ManagedTable) ToOutput() ManagedTableOutput {
	return ManagedTableOutput{
		ID:           mt.ID,
		ConnectionID: mt.ConnectionID,
		TableName:    mt.TableName,
		SchemaName:   mt.SchemaName,
	}
}
