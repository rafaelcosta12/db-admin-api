package repositories

import (
	"db-admin/models/entities"

	"github.com/google/uuid"
)

type IRepository interface {
	GetById(id uuid.UUID) (*entities.IEntity, error)
	Save(entity *entities.IEntity) error
	Delete(entity *entities.Entity) error
	GetAll() (*[]*entities.IEntity, error)
}

type BaseRepository struct {
	IRepository
}
