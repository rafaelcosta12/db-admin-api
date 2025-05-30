package repositories

import (
	"db-admin/core"
	"db-admin/models/entities"

	"github.com/google/uuid"
)

func GetManagedTables() ([]entities.ManagedTable, error) {
	var managedTables []entities.ManagedTable
	query := "SELECT id, connection_id, table_name, schema_name FROM managed_tables"
	err := core.AppDB.Select(&managedTables, query)
	if err != nil {
		return nil, err
	}

	return managedTables, nil
}

func GetManagedTablesByConnection(connectionId uuid.UUID) ([]entities.ManagedTable, error) {
	var managedTables []entities.ManagedTable
	query := "SELECT id, connection_id, table_name, schema_name FROM managed_tables WHERE connection_id = $1"
	err := core.AppDB.Select(&managedTables, query, connectionId)
	if err != nil {
		return nil, err
	}

	return managedTables, nil
}

func CreateManagedTable(table entities.ManagedTable) (entities.ManagedTable, error) {
	query := "INSERT INTO managed_tables (id, connection_id, table_name, schema_name) VALUES ($1, $2, $3, $4) RETURNING id"
	err := core.AppDB.QueryRow(query, table.ID, table.ConnectionID, table.TableName, table.SchemaName).Scan(&table.ID)
	if err != nil {
		return entities.ManagedTable{}, err
	}

	return table, nil
}
