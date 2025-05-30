package repositories

import (
	"db-admin/core"
	"db-admin/models/dto"
	"db-admin/models/entities"
)

func CreateUserGroup(userGroup entities.UserGroup) (entities.UserGroup, error) {
	var query = `
	INSERT INTO user_groups 
	(name, created_at, updated_at) 
	VALUES 
	($1, $2, $3)
	RETURNING id`

	err := core.AppDB.QueryRow(query, userGroup.Name, userGroup.CreatedAt, userGroup.UpdatedAt).Scan(&userGroup.ID)
	if err != nil {
		return entities.UserGroup{}, err
	}

	return userGroup, nil
}

func UpdateUserGroup(userGroup entities.UserGroup) (entities.UserGroup, error) {
	var query = `
	UPDATE user_groups 
	SET 
		name = $1, 
		updated_at = $2
	WHERE id = $3
	RETURNING id`

	err := core.AppDB.QueryRow(query, userGroup.Name, userGroup.UpdatedAt, userGroup.ID).Scan(&userGroup.ID)
	if err != nil {
		return entities.UserGroup{}, err
	}

	return userGroup, nil
}

func GetUserGroupByID(id int) (entities.UserGroup, error) {
	var userGroup entities.UserGroup
	err := core.AppDB.Get(&userGroup, "SELECT * FROM user_groups WHERE id = $1", id)
	if err != nil {
		return entities.UserGroup{}, err
	}
	return userGroup, nil
}

func GetAllUserGroups() ([]entities.UserGroup, error) {
	var userGroups []entities.UserGroup
	err := core.AppDB.Select(&userGroups, "SELECT * FROM user_groups")
	if err != nil {
		return nil, err
	}
	return userGroups, nil
}

func DeleteUserGroup(id int) error {
	var query = `
	DELETE FROM user_groups 
	WHERE id = $1`

	_, err := core.AppDB.Exec(query, id)
	if err != nil {
		return err
	}

	return nil
}

func AddUserToGroup(input dto.UserGroupMember) (dto.UserGroupMember, error) {
	var query = `
	INSERT INTO user_group_membership 
	(user_id, group_id, created_at, updated_at) 
	VALUES 
	($1, $2, $3, $4)
	RETURNING id`

	err := core.AppDB.QueryRow(query, input.UserID, input.UserGroupID, input.CreatedAt, input.UpdatedAt).Scan(&input.ID)
	if err != nil {
		return dto.UserGroupMember{}, err
	}

	return input, nil
}

func RemoveUserFromGroup(userId, groupId int) error {
	var query = `
	DELETE FROM user_group_membership 
	WHERE user_id = $1 AND group_id = $2`

	_, err := core.AppDB.Exec(query, userId, groupId)
	if err != nil {
		return err
	}

	return nil
}

func GetUserGroupMembers(groupId int) ([]entities.User, error) {
	var members []entities.User
	err := core.AppDB.Select(&members, "SELECT u.* FROM user_group_membership m INNER JOIN users u ON u.id = m.user_id WHERE m.group_id = $1", groupId)
	if err != nil {
		return nil, err
	}
	return members, nil
}
