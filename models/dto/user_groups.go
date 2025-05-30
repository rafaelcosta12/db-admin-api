package dto

import (
	"db-admin/models/entities"
	"time"
)

type UserGroupMember struct {
	ID          int       `db:"id" json:"id"`
	UserID      int       `db:"user_id" json:"user_id"`
	UserGroupID int       `db:"group_id" json:"user_group_id"`
	CreatedAt   time.Time `db:"created_at" json:"created_at"`
	UpdatedAt   time.Time `db:"updated_at" json:"updated_at"`
}

type UserGroupCreate struct {
	Name string `json:"name" binding:"required"`
}

type UserGroupUpdate struct {
	Name string `json:"name" binding:"required"`
}

type UserGroupOutput struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type UserGroupMemberOutput struct {
	ID          int `json:"id"`
	UserID      int `json:"user_id"`
	UserGroupID int `json:"user_group_id"`
}

func ToUserGroupOutput(ug *entities.UserGroup) UserGroupOutput {
	return UserGroupOutput{
		ID:   ug.ID,
		Name: ug.Name,
	}
}

func (ugc *UserGroupCreate) ToUserGroup() entities.UserGroup {
	return entities.UserGroup{
		Name:      ugc.Name,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
}

func (ugc *UserGroupUpdate) Update(ug *entities.UserGroup) {
	ug.Name = ugc.Name
	ug.UpdatedAt = time.Now()
}

func (ugm *UserGroupMember) ToOutput() UserGroupMemberOutput {
	return UserGroupMemberOutput{
		ID:          ugm.ID,
		UserID:      ugm.UserID,
		UserGroupID: ugm.UserGroupID,
	}
}
