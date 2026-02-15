-- init.sql
-- Create additional tables or insert sample data

-- Create sample table
CREATE TABLE IF NOT EXISTS sample_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    value INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO sample_data (name, value) VALUES
    ('Item 1', 100),
    ('Item 2', 200),
    ('Item 3', 300),
    ('Item 4', 400),
    ('Item 5', 500)
ON CONFLICT DO NOTHING;

-- Create user table for demo
CREATE TABLE IF NOT EXISTS demo_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pythonuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pythonuser;