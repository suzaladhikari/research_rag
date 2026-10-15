CREATE TABLE documents (
    file_id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'uploaded',
    uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    
);