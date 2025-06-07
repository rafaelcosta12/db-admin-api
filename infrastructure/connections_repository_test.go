package infrastructure

import (
	"testing"

	"db-admin/core"
	"db-admin/models/entities/connection"

	"github.com/stretchr/testify/assert"
)

func TestConnectionRepository_CRUD_Success(t *testing.T) {
	core.ConfigureAppDB()
	repo := &ConnectionRepository{}

	newConnection, err := connection.NewConnection("postgres://user:password@localhost:5432/dbname", "TestConnection")
	assert.NoError(t, err)

	err = repo.Save(newConnection)
	assert.NoError(t, err)

	connection, err := repo.GetById(newConnection.ID)
	assert.NoError(t, err)
	assert.Equal(t, "TestConnection", connection.Name)
	assert.Equal(t, "postgres://user:password@localhost:5432/dbname", connection.ConnectionString.String())

	// get all connections
	connections, err := repo.GetAll()
	assert.NoError(t, err)
	assert.NotEmpty(t, connections)

	connection.Name = "UpdatedConnection"
	err = repo.Save(connection)
	assert.NoError(t, err)

	connection, err = repo.GetById(connection.ID)
	assert.NoError(t, err)
	assert.Equal(t, "UpdatedConnection", connection.Name)

	err = repo.Delete(connection)
	assert.NoError(t, err)

	_, err = repo.GetById(connection.ID)
	assert.Error(t, err) // Expect an error since the connection was deleted
}
