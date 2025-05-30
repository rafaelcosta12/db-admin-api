package dto

import (
	"db-admin/models/entities"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type UserOrderBy string

const (
	EmailOrderBy     UserOrderBy = "email"
	NameOrderBy      UserOrderBy = "name"
	CreatedAtOrderBy UserOrderBy = "created_at"
	UpdatedAtOrderBy UserOrderBy = "updated_at"
	IsAdminOrderBy   UserOrderBy = "is_admin"
	IsActiveOrderBy  UserOrderBy = "is_active"
)

type UserSearch struct {
	Limit    int
	Offset   int
	Order    Order
	Text     string
	OrderBy  UserOrderBy
	IsActive *bool
	IsAdmin  *bool
}

type UserCreate struct {
	Email      string  `db:"email" json:"email" binding:"required"`
	Name       string  `db:"name" json:"name" binding:"required"`
	Password   string  `db:"password" json:"password" binding:"required"`
	IsAdmin    bool    `db:"is_admin" json:"is_admin"`
	IsActive   bool    `db:"is_active" json:"is_active"`
	ProfileImg *string `db:"profile_img" json:"profile_img"`
}

type UserUpdate struct {
	Name       string  `db:"name" json:"name"`
	IsAdmin    bool    `db:"is_admin" json:"is_admin"`
	IsActive   bool    `db:"is_active" json:"is_active"`
	ProfileImg *string `db:"profile_img" json:"profile_img"`
}

type UserOutput struct {
	ID         int       `db:"id" json:"id"`
	Email      string    `db:"email" json:"email"`
	Name       string    `db:"name" json:"name"`
	CreatedAt  time.Time `db:"created_at" json:"created_at"`
	UpdatedAt  time.Time `db:"updated_at" json:"updated_at"`
	IsAdmin    bool      `db:"is_admin" json:"is_admin"`
	IsActive   bool      `db:"is_active" json:"is_active"`
	ProfileImg *string   `db:"profile_img" json:"profile_img"`
}

func (u *UserCreate) ToUser() (entities.User, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return entities.User{}, err
	}

	return entities.User{
		Email:      u.Email,
		Name:       u.Name,
		Password:   string(hashedPassword),
		IsAdmin:    u.IsAdmin,
		IsActive:   u.IsActive,
		CreatedAt:  time.Now(),
		UpdatedAt:  time.Now(),
		ProfileImg: u.ProfileImg,
	}, nil
}

func UpdateUser(u *entities.User, userUpdate UserUpdate) *entities.User {
	u.Name = userUpdate.Name
	u.IsAdmin = userUpdate.IsAdmin
	u.IsActive = userUpdate.IsActive
	u.ProfileImg = userUpdate.ProfileImg
	u.UpdatedAt = time.Now()
	return u
}

func ToUserOutput(u *entities.User) UserOutput {
	return UserOutput{
		ID:         u.ID,
		Email:      u.Email,
		Name:       u.Name,
		IsAdmin:    u.IsAdmin,
		IsActive:   u.IsActive,
		CreatedAt:  u.CreatedAt,
		UpdatedAt:  u.UpdatedAt,
		ProfileImg: u.ProfileImg,
	}
}
