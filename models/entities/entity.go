package entities

import "github.com/google/uuid"

type IEntity interface {
	GetID() uuid.UUID
}

type Entity struct {
	IEntity
	ID uuid.UUID `db:"id" json:"id"`
}

func (e *Entity) GetID() uuid.UUID {
	return e.ID
}
