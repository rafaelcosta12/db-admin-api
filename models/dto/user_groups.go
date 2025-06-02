package dto

import (
	"db-admin/models/entities"
	"time"
)

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

func ToUserGroupMemberOutput(ugm *entities.UserGroupMember) UserGroupMemberOutput {
	return UserGroupMemberOutput{
		ID:          ugm.ID,
		UserID:      ugm.UserID,
		UserGroupID: ugm.UserGroupID,
	}
}
