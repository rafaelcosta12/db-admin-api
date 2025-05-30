package repositories

import (
	"db-admin/core"
	"db-admin/models/configurations"
	"db-admin/models/database"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
)

// restrictedSchemas defines a list of PostgreSQL system schemas that are considered restricted.
// These schemas typically contain internal database metadata and system information, and are
// excluded from operations that should not affect system-level objects.
var restrictedSchemas = []string{
	"information_schema",
	"pg_catalog",
	"pg_internal",
}

func GetConnectionByID(connectionID uuid.UUID) (configurations.Connection, error) {
	return core.GetConnectionByID(connectionID)
}

func CreateConnection(connection configurations.Connection) (configurations.Connection, error) {
	return core.CreateConnection(connection)
}

func UpdateConnection(connectionID uuid.UUID, connection configurations.Connection) (configurations.Connection, error) {
	return core.UpdateConnection(connectionID, connection)
}

func DeleteConnection(connectionID uuid.UUID) error {
	return core.DeleteConnection(connectionID)
}

func GetAllConnections() ([]configurations.Connection, error) {
	connections := []configurations.Connection{}
	err := core.AppDB.Select(&connections, "SELECT id, driver, connection_string, name FROM connections")
	if err != nil {
		return nil, err
	}
	return connections, nil
}

func GetSchemas(connectionID uuid.UUID) ([]database.Schema, error) {
	var schemas []database.Schema
	conn, err := core.GetDB(connectionID)
	if err != nil {
		return nil, err
	}

	query, args, err := sqlx.In("SELECT DISTINCT table_schema FROM information_schema.tables WHERE table_schema NOT IN (?)", restrictedSchemas)
	if err != nil {
		return nil, err
	}
	query = conn.Rebind(query)

	err = conn.Select(&schemas, query, args...)
	if err != nil {
		return nil, err
	}

	err = fetchTablesForSchemas(&schemas, conn)
	if err != nil {
		return nil, err
	}

	return schemas, nil
}

func GetTables(connectionID uuid.UUID, schemas []string, tables []string) ([]database.Table, error) {
	conn, err := core.GetDB(connectionID)
	if err != nil {
		return nil, err
	}

	query, args, err := sqlx.In("SELECT DISTINCT table_name, table_schema FROM information_schema.tables WHERE table_schema NOT IN (?) AND table_schema IN (?) AND table_name IN (?)", restrictedSchemas, schemas, tables)
	if err != nil {
		return nil, err
	}
	query = conn.Rebind(query)

	var allTables []database.Table
	err = conn.Select(&allTables, query, args...)
	if err != nil {
		return nil, err
	}

	err = fetchColumnsForTables(&allTables, conn)
	if err != nil {
		return nil, err
	}

	return allTables, nil
}

func fetchTablesForSchemas(schemas *[]database.Schema, conn *sqlx.DB) error {
	schemasNames := []string{}
	for _, schema := range *schemas {
		schemasNames = append(schemasNames, schema.Name)
	}

	query, args, err := sqlx.In("SELECT DISTINCT table_name, table_schema FROM information_schema.tables WHERE table_schema IN (?)", schemasNames)
	if err != nil {
		return err
	}
	query = conn.Rebind(query)

	var allTables []database.Table
	err = conn.Select(&allTables, query, args...)
	if err != nil {
		return err
	}

	for i := range *schemas {
		schema := &(*schemas)[i]
		for _, table := range allTables {
			if table.SchemaName == schema.Name {
				schema.Tables = append(schema.Tables, table)
			}
		}

		err = fetchColumnsForTables(&schema.Tables, conn)
		if err != nil {
			return err
		}
	}

	return nil
}

func fetchColumnsForTables(tables *[]database.Table, conn *sqlx.DB) error {
	tablesNames := []string{}
	for _, table := range *tables {
		tablesNames = append(tablesNames, table.Name)
	}

	query, args, err := sqlx.In("SELECT table_name, column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name IN (?) ORDER BY ordinal_position", tablesNames)
	if err != nil {
		return err
	}
	query = conn.Rebind(query)

	var allColumns []database.Column
	err = conn.Select(&allColumns, query, args...)
	if err != nil {
		return err
	}

	for i := range *tables {
		table := &(*tables)[i]
		for _, column := range allColumns {
			if column.TableName == table.Name {
				(*table).Columns = append(table.Columns, column)
			}
		}
	}
	return nil
}
