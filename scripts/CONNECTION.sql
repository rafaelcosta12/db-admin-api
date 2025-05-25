CREATE TABLE connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_string TEXT NOT NULL,
    name TEXT NOT NULL,
    driver TEXT NOT NULL
);