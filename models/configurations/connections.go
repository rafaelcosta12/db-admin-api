package configurations

import "github.com/google/uuid"

type Connection struct {
	ID               uuid.UUID `db:"id"`
	ConnectionString string    `db:"connection_string"`
	Name             string    `db:"name"`
	Driver           string    `db:"driver"`
}

type ConnectionCreate struct {
	ConnectionString string `json:"connection_string" binding:"required"`
	Name             string `json:"name" binding:"required"`
	Driver           string `json:"driver" binding:"required"`
}

type ConnectionUpdate struct {
	ConnectionCreate
}

type ConnectionOutput struct {
	ID               uuid.UUID `json:"id"`
	ConnectionString string    `json:"connection_string"`
	Name             string    `json:"name"`
	Driver           string    `json:"driver"`
}

func (c *ConnectionCreate) ToConnection() Connection {
	return Connection{
		ID:               uuid.New(),
		ConnectionString: c.ConnectionString,
		Name:             c.Name,
		Driver:           c.Driver,
	}
}

func (c *Connection) Update(d ConnectionUpdate) {
	c.ConnectionString = d.ConnectionString
	c.Name = d.Name
	c.Driver = d.Driver
}

func (c Connection) ToOutput() ConnectionOutput {
	return ConnectionOutput{
		ID:               c.ID,
		ConnectionString: "********", // Mask sensitive data
		Name:             c.Name,
		Driver:           c.Driver,
	}
}
