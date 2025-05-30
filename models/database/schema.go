package database

type Schema struct {
	Name   string `db:"table_schema"`
	Tables []Table
}

type SchemaOutput struct {
	Name   string        `json:"name"`
	Tables []TableOutput `json:"tables"`
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
