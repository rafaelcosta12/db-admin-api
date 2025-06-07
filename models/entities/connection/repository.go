package connection

import "github.com/google/uuid"

type Repository interface {
	GetByID(id uuid.UUID) (*Connection, error)
	Save(entity *Connection) error
	Delete(entity *Connection) error
	GetAll() (*[]*Connection, error)
}
