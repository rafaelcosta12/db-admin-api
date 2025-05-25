package repositories

import (
	"db-admin/core"
	"db-admin/models"
)

func GetUserByID(id int) (models.User, error) {
	var user models.User
	err := core.AppDB.Get(&user, "SELECT * FROM users WHERE id = $1", id)
	if err != nil {
		return models.User{}, err
	}
	return user, nil
}

func GetUsers(search models.UserSearch) ([]models.User, error) {
	var users []models.User
	var query = `
	SELECT * FROM users
	`
	if search.Text != "" {
		query += `WHERE email ILIKE $1 OR name ILIKE $1`
	}

	if search.IsActive != nil {
		if *search.IsActive {
			query += ` AND is_active = true`
		} else {
			query += ` AND is_active = false`
		}
	}

	if search.IsAdmin != nil {
		if *search.IsAdmin {
			query += ` AND is_admin = true`
		} else {
			query += ` AND is_admin = false`
		}
	}

	if search.Order != "" {
		query += ` ORDER BY $4 ` + string(search.Order)
	}

	if search.Limit > 0 {
		query += ` LIMIT $2 OFFSET $3`
	}

	err := core.AppDB.Select(&users, query, search.Text, search.Limit, search.Offset, search.OrderBy)
	if err != nil {
		return nil, err
	}
	return users, nil
}

func GetUserByEmail(email string) (models.User, error) {
	var user models.User
	err := core.AppDB.Get(&user, "SELECT * FROM users WHERE email = $1", email)
	if err != nil {
		return models.User{}, err
	}
	return user, nil
}

func CreateUser(user models.User) (models.User, error) {
	var query = `
	INSERT INTO users 
	(email, name, password, is_active, is_admin, created_at, updated_at, profile_img) 
	VALUES 
	($1, $2, $3, $4, $5, $6, $7, $8)
	RETURNING id`

	err := core.AppDB.QueryRow(query, user.Email, user.Name, user.Password, user.IsActive, user.IsAdmin, user.CreatedAt, user.UpdatedAt, user.ProfileImg).Scan(&user.ID)
	if err != nil {
		return models.User{}, err
	}

	return user, nil
}

func UpdateUser(user models.User) (models.User, error) {
	var query = `
	UPDATE users 
	SET 
		email = $1, 
		name = $2, 
		password = $3, 
		is_active = $4, 
		is_admin = $5, 
		updated_at = $6, 
		profile_img = $7
	WHERE id = $8
	RETURNING id`

	err := core.AppDB.QueryRow(query, user.Email, user.Name, user.Password, user.IsActive, user.IsAdmin, user.UpdatedAt, user.ProfileImg, user.ID).Scan(&user.ID)
	if err != nil {
		return models.User{}, err
	}

	return user, nil
}

func DeleteUser(id int) error {
	var query = `
	DELETE FROM users 
	WHERE id = $1`

	_, err := core.AppDB.Exec(query, id)
	if err != nil {
		return err
	}

	return nil
}
