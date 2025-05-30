-- Quero criar uma tabela para linkar uma tabela existente pelo nome/schema a uma connection, e que tenha um id guid
CREATE TABLE managed_tables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_id UUID NOT NULL,
    table_name NAME NOT NULL, -- mesmo tipo da coluna information_schema.tables.table_name
    schema_name NAME NOT NULL,
    FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE,
    UNIQUE (connection_id, table_name, schema_name)
);

-- Exemplo de inserção:
-- INSERT INTO managed_tables (connection_id, table_name, schema_name)
-- VALUES ('<connection_id>', 'my_table', 'public');
-- Exemplo de consulta:
-- SELECT * FROM managed_tables WHERE connection_id = '<connection_id>';
-- Exemplo de atualização:
-- UPDATE managed_tables
-- SET table_name = 'new_table_name'
-- WHERE id = '<managed_table_id>';
-- Exemplo de deleção:
-- DELETE FROM managed_tables WHERE id = '<managed_table_id>';
-- Exemplo de consulta para listar todas as tabelas gerenciadas por uma conexão específica:
-- SELECT * FROM managed_tables WHERE connection_id = '<connection_id>';
-- Exemplo de consulta para listar todas as tabelas gerenciadas:
-- SELECT * FROM managed_tables;

CREATE TABLE managed_table_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    managed_table_id INT NOT NULL,
    user_group UUID NOT NULL,
    permission_type VARCHAR(50) NOT NULL, -- Exemplo: 'read', 'write', 'admin'
    FOREIGN KEY (managed_table_id) REFERENCES managed_tables(id) ON DELETE CASCADE,
    FOREIGN KEY (user_group) REFERENCES user_groups(id) ON DELETE CASCADE,
    UNIQUE (managed_table_id, user_group)
);
