package core

import (
	"database/sql"
	"db-admin/models"
	"log"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq" // Driver PostgreSQL
)

var AppDB *sqlx.DB

func ConfigureAppDB() {
	var err error
	AppDB, err = sqlx.Connect("postgres", "user=postgres password=postgres dbname=devstacker sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}
	// Otimiza o pool para APIs REST
	AppDB.SetMaxOpenConns(25)                  // Máximo de conexões ativas
	AppDB.SetMaxIdleConns(5)                   // Conexões mantidas ociosas
	AppDB.SetConnMaxLifetime(30 * time.Minute) // Tempo máximo de vida
}

var connectedDBs = map[uuid.UUID]*sqlx.DB{}
var mu sync.Mutex

func connectDB(connection models.Connection) (*sqlx.DB, error) {
	var err error
	db, err := sqlx.Connect("postgres", connection.ConnectionString)
	if err != nil {
		return nil, err
	}
	// Otimiza o pool para APIs REST
	db.SetMaxOpenConns(25)                  // Máximo de conexões ativas
	db.SetMaxIdleConns(5)                   // Conexões mantidas ociosas
	db.SetConnMaxLifetime(30 * time.Minute) // Tempo máximo de vida
	connectedDBs[connection.ID] = db
	return db, nil
}

func GetConnectionByID(id uuid.UUID) (models.Connection, error) {
	var connection models.Connection
	err := AppDB.Get(&connection, "SELECT id, driver, connection_string, name FROM connections WHERE id = $1", id)
	if err != nil {
		return models.Connection{}, err
	}
	return connection, nil
}

func CreateConnection(connection models.Connection) (models.Connection, error) {
	connection.ID = uuid.New()
	_, err := AppDB.NamedExec("INSERT INTO connections (id, driver, connection_string, name) VALUES (:id, :driver, :connection_string, :name)", connection)
	if err != nil {
		return models.Connection{}, err
	}
	return connection, nil
}

func DeleteConnection(id uuid.UUID) error {
	_, err := AppDB.Exec("DELETE FROM connections WHERE id = $1", id)
	if err != nil {
		return err
	}
	mu.Lock()
	defer mu.Unlock()
	delete(connectedDBs, id)
	return nil
}

func UpdateConnection(id uuid.UUID, connection models.Connection) (models.Connection, error) {
	_, err := AppDB.NamedExec("UPDATE connections SET driver = :driver, connection_string = :connection_string, name = :name WHERE id = :id", connection)
	if err != nil {
		return models.Connection{}, err
	}
	mu.Lock()
	defer mu.Unlock()
	connectedDBs[id] = nil // Remove the cached connection
	return connection, nil
}

func GetDB(id uuid.UUID) (*sqlx.DB, error) {
	mu.Lock()
	defer mu.Unlock()

	if db, ok := connectedDBs[id]; ok {
		return db, nil
	}

	connection, err := GetConnectionByID(id)
	if err != nil {
		if err == sql.ErrNoRows {
			log.Printf("No connection found for id: %d", id)
			return nil, err
		}
		log.Printf("Error fetching connection: %v", err)
		return nil, err
	}

	return connectDB(connection)
}
