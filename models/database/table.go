package database

type Table struct {
	Name       string `db:"table_name"`
	SchemaName string `db:"table_schema"`
	Columns    []Column
}

type TableOutput struct {
	Name    string         `json:"name"`
	Schema  string         `json:"schema"`
	Columns []ColumnOutput `json:"columns"`
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
