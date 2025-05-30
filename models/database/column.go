package database

type Column struct {
	Name         string  `db:"column_name"`
	TableName    string  `db:"table_name"` // json ignored to avoid redundancy
	DataType     string  `db:"data_type"`
	Nullable     string  `db:"is_nullable"`
	DefaultValue *string `db:"column_default"`
}

type ColumnOutput struct {
	Name         string  `json:"name"`
	DataType     string  `json:"data_type"`
	Nullable     bool    `json:"nullable"`
	DefaultValue *string `json:"default_value"`
}

func (c *Column) ToOutput() ColumnOutput {
	output := ColumnOutput{
		Name:         c.Name,
		DataType:     c.DataType,
		Nullable:     c.Nullable == "YES", // Convert to boolean
		DefaultValue: c.DefaultValue,
	}
	return output
}
