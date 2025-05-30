package entities

import "time"

type User struct {
	ID         int       `db:"id" json:"id"`
	Email      string    `db:"email" json:"email"`
	Name       string    `db:"name" json:"name"`
	Password   string    `db:"password" json:"password"`
	CreatedAt  time.Time `db:"created_at" json:"created_at"`
	UpdatedAt  time.Time `db:"updated_at" json:"updated_at"`
	IsAdmin    bool      `db:"is_admin" json:"is_admin"`
	IsActive   bool      `db:"is_active" json:"is_active"`
	ProfileImg *string   `db:"profile_img" json:"profile_img"`
}
