package dto

import (
	"db-admin/models/database"
	"db-admin/models/entities"

	"github.com/google/uuid"
)

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

func (m *ManagedTableCreate) ToManagedTable() entities.ManagedTable {
	return entities.ManagedTable{
		ID:           uuid.New(),
		ConnectionID: m.ConnectionID,
		TableName:    m.TableName,
		SchemaName:   m.SchemaName,
	}
}

func ToManagedTableOutput(mt *entities.ManagedTable) ManagedTableOutput {
	return ManagedTableOutput{
		ID:           mt.ID,
		ConnectionID: mt.ConnectionID,
		TableName:    mt.TableName,
		SchemaName:   mt.SchemaName,
	}
}
