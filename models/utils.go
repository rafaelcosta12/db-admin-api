package models

type Order string

const (
	Asc  Order = "ASC"
	Desc Order = "DESC"
)

type Pagination struct {
	Total int   `json:"total"`
	Page  int   `json:"page"`
	Items []any `json:"items"`
}
