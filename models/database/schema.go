package database

type Schema struct {
	Name   string `db:"table_schema"`
	Tables []Table
}

type Table struct {
	Name       string `db:"table_name"`
	SchemaName string `db:"table_schema"`
	Columns    []Column
}

type Column struct {
	Name         string  `db:"column_name"`
	TableName    string  `db:"table_name"` // json ignored to avoid redundancy
	DataType     string  `db:"data_type"`
	Nullable     string  `db:"is_nullable"`
	DefaultValue *string `db:"column_default"`
}

type SchemaOutput struct {
	Name   string        `json:"name"`
	Tables []TableOutput `json:"tables"`
}

type TableOutput struct {
	Name    string         `json:"name"`
	Schema  string         `json:"schema"`
	Columns []ColumnOutput `json:"columns"`
}

type ColumnOutput struct {
	Name         string  `json:"name"`
	DataType     string  `json:"data_type"`
	Nullable     bool    `json:"nullable"`
	DefaultValue *string `json:"default_value"`
}

func (s *Schema) ToOutput() SchemaOutput {
	output := SchemaOutput{
		Name: s.Name,
	}

	for _, table := range s.Tables {
		output.Tables = append(output.Tables, table.ToOutput())
	}

	return output
}

func (t *Table) ToOutput() TableOutput {
	output := TableOutput{
		Name:   t.Name,
		Schema: t.SchemaName,
	}

	for _, column := range t.Columns {
		output.Columns = append(output.Columns, column.ToOutput())
	}

	return output
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
