package dto

type LoginResponse struct {
	Token  string `json:"token"`
	Prefix string `json:"prefix"`
}

type UserLogin struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

type UserToken struct {
	ID      int    `json:"id"`
	Email   string `json:"email"`
	Name    string `json:"name"`
	IsAdmin bool   `json:"is_admin"`
}
