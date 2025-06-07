-- drop table public.managed_table_permissions;
-- drop table public.managed_tables;
-- drop table public.connections;

CREATE TABLE public.connections (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	connection_string text NOT NULL,
	"name" text NOT NULL,
	CONSTRAINT connections_pkey PRIMARY KEY (id)
);

CREATE TABLE public.managed_tables (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	connection_id uuid NOT NULL,
	table_name name COLLATE "C" NOT NULL,
	schema_name name COLLATE "C" NOT NULL,
	CONSTRAINT managed_tables_connection_id_table_name_schema_name_key UNIQUE (connection_id, table_name, schema_name),
	CONSTRAINT managed_tables_pkey PRIMARY KEY (id)
);

CREATE TABLE public.managed_table_permissions (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	managed_table_id uuid NOT NULL,
	user_group int4 NOT NULL,
	permission_type varchar(50) NOT NULL,
	CONSTRAINT managed_table_permissions_managed_table_id_user_group_key UNIQUE (managed_table_id, user_group),
	CONSTRAINT managed_table_permissions_pkey PRIMARY KEY (id)
);