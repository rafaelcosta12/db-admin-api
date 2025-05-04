from sqlalchemy import create_engine, MetaData, inspect

# Criar engine e conectar
engine = create_engine("postgresql://postgres:postgres@localhost:5432/devstacker")
connection = engine.connect()

# Criar objeto de metadados
metadata = MetaData()

# Refletir todas as tabelas do banco de dados
metadata.reflect(bind=engine)

# Criar inspetor para obter informações detalhadas
inspector = inspect(engine)

for schema in inspector.get_schema_names():
    print(f"\nSchema: {schema}")
    # Obter informações sobre as tabelas no schema
    tables = inspector.get_table_names(schema=schema)
    print(f"Tabelas no schema {schema}:")
    for table in tables:
        # 1. Listar todas as tabelas
        print("Tabelas no banco de dados:")
        tables = inspector.get_table_names()
        for table in tables:
            print(f"- {table}")

            # 2. Obter colunas de cada tabela
            columns = inspector.get_columns(table)
            print(f"\nColunas da tabela {table}:")
            for column in columns:
                print(f"  Nome: {column['name']}")
                print(f"  Tipo: {column['type']}")
                print(f"  Nulo: {'Sim' if column['nullable'] else 'Não'}")
                print(f"  Default: {column['default']}")
                # print(f"  Chave primária: {'Sim' if column['primary_key'] else 'Não'}")
                print("  ---")

            # 3. Obter chaves primárias
            primary_keys = inspector.get_pk_constraint(table)
            print(f"\nChaves primárias da tabela {table}: {primary_keys['constrained_columns']}")

            # 4. Obter chaves estrangeiras
            foreign_keys = inspector.get_foreign_keys(table)
            if foreign_keys:
                print(f"\nChaves estrangeiras da tabela {table}:")
                for fk in foreign_keys:
                    print(f"  Nome: {fk['name']}")
                    print(f"  Colunas: {fk['constrained_columns']}")
                    print(f"  Tabela de referência: {fk['referred_table']}")
                    print(f"  Colunas de referência: {fk['referred_columns']}")
                    # print(f"  On delete: {fk['ondelete']}")
                    # print(f"  On update: {fk['onupdate']}")
                    print("  ---")
            else:
                print(f"\nTabela {table} não possui chaves estrangeiras")

            # 5. Obter índices
            indexes = inspector.get_indexes(table)
            if indexes:
                print(f"\nÍndices da tabela {table}:")
                for index in indexes:
                    print(f"  Nome: {index['name']}")
                    print(f"  Colunas: {index['column_names']}")
                    print(f"  Único: {'Sim' if index['unique'] else 'Não'}")
                    print("  ---")
            else:
                print(f"\nTabela {table} não possui índices")

            # # 6. Obter restrições de verificação (check constraints)
            # # Nota: O inspector padrão do SQLAlchemy não tem método direto para check constraints
            # # Podemos usar uma consulta SQL diretamente
            # check_constraints = connection.execute(f"""
            #     SELECT conname, consrc 
            #     FROM pg_constraint
            #     JOIN pg_class ON pg_constraint.conrelid = pg_class.oid
            #     WHERE pg_class.relname = '{table}' AND pg_constraint.contype = 'c'
            # """).fetchall()
            
            # if check_constraints:
            #     print(f"\nCheck constraints da tabela {table}:")
            #     for constraint in check_constraints:
            #         print(f"  Nome: {constraint[0]}")
            #         print(f"  Condição: {constraint[1]}")
            #         print("  ---")
            # else:
            #     print(f"\nTabela {table} não possui check constraints")

            print("\n" + "="*50 + "\n")



# Fechar conexão
connection.close()
engine.dispose()