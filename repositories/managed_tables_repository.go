package repositories

import (
	"db-admin/core"
	"db-admin/models/configurations"

	"github.com/google/uuid"
)

func GetManagedTables() ([]configurations.ManagedTable, error) {
	var managedTables []configurations.ManagedTable
	query := "SELECT id, connection_id, table_name, schema_name FROM managed_tables"
	err := core.AppDB.Select(&managedTables, query)
	if err != nil {
		return nil, err
	}

	return managedTables, nil
}

func GetManagedTablesByConnection(connectionId uuid.UUID) ([]configurations.ManagedTable, error) {
	var managedTables []configurations.ManagedTable
	query := "SELECT id, connection_id, table_name, schema_name FROM managed_tables WHERE connection_id = $1"
	err := core.AppDB.Select(&managedTables, query, connectionId)
	if err != nil {
		return nil, err
	}

	return managedTables, nil
}

func CreateManagedTable(table configurations.ManagedTable) (configurations.ManagedTable, error) {
	query := "INSERT INTO managed_tables (id, connection_id, table_name, schema_name) VALUES ($1, $2, $3, $4) RETURNING id"
	err := core.AppDB.QueryRow(query, table.ID, table.ConnectionID, table.TableName, table.SchemaName).Scan(&table.ID)
	if err != nil {
		return configurations.ManagedTable{}, err
	}

	return table, nil
}
