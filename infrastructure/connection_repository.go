package infrastructure

import (
	"db-admin/core"
	"db-admin/models/entities/connection"
	"db-admin/repositories/tables"

	"github.com/google/uuid"
)

type ConnectionRepository struct {
	connection.Repository
}

var getByIdQuery = `SELECT id, connection_string, name FROM connections WHERE id = $1`

func (repo *ConnectionRepository) GetById(id uuid.UUID) (*connection.Connection, error) {
	var c tables.ConnectionTable
	err := core.AppDB.Get(&c, getByIdQuery, id)
	if err != nil {
		return nil, err
	}
	return tables.FromConnectionTable(&c)
}

var saveQuery = `
INSERT INTO connections (id, connection_string, name)
VALUES (:id, :connection_string, :name)
ON CONFLICT (id) DO UPDATE
SET connection_string = :connection_string,
	name = :name
`

func (repo *ConnectionRepository) Save(entity *connection.Connection) error {
	_, err := core.AppDB.NamedExec(saveQuery, tables.ToConnectionTable(entity))
	if err != nil {
		return err
	}
	return nil
}

var deleteQuery = `DELETE FROM connections WHERE id = :id`

func (repo *ConnectionRepository) Delete(entity *connection.Connection) error {
	_, err := core.AppDB.NamedExec(deleteQuery, tables.ToConnectionTable(entity))
	if err != nil {
		return err
	}
	return nil
}

var getAllQuery = `SELECT id, connection_string, name FROM connections`

func (repo *ConnectionRepository) GetAll() (*[]*connection.Connection, error) {
	var connections []tables.ConnectionTable

	err := core.AppDB.Select(&connections, getAllQuery)
	if err != nil {
		return nil, err
	}

	var dest []*connection.Connection
	for _, c := range connections {
		a, err := tables.FromConnectionTable(&c)
		if err != nil {
			continue
		}
		dest = append(dest, a)
	}

	return &dest, nil
}
