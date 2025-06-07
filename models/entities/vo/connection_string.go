// domain/database/connection_string.go
package vo

import (
	"fmt"
	"net/url"
	"slices"
)

// ConnectionString é um Value Object que encapsula e valida strings de conexão para SQLx
type ConnectionString struct {
	value url.URL
}

var possibleDrivers = []string{"postgres", "mysql", "sqlite", "sqlserver", "oracle"}

// NewConnectionString cria uma nova ConnectionString validada
func NewConnectionString(rawConnStr string) (ConnectionString, error) {
	u, err := url.Parse(rawConnStr)

	if err != nil {
		return ConnectionString{}, err
	}

	if u.Scheme == "" {
		return ConnectionString{}, fmt.Errorf("invalid connection string: missing scheme")
	}

	if !slices.Contains(possibleDrivers, u.Scheme) {
		return ConnectionString{}, fmt.Errorf("invalid connection string: unsupported driver '%s'", u.Scheme)
	}

	if u.Host == "" {
		return ConnectionString{}, fmt.Errorf("invalid connection string: missing host")
	}

	if u.Path == "" {
		return ConnectionString{}, fmt.Errorf("invalid connection string: missing path")
	}

	return ConnectionString{value: *u}, nil
}

func (cs ConnectionString) String() string {
	return cs.value.String()
}

func (cs ConnectionString) Value() url.URL {
	return cs.value
}
