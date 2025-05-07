CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Example insert with password hash (for testing purposes, this should be done dynamically in your app)
-- INSERT INTO users (name, email, password_hash) VALUES ('Rick', 'rick@example.com', 'hashed_password_here');
