CREATE TABLE documents (
    file_id TEXT PRIMARY KEY,  -- For the file id 
    file_name TEXT NOT NULL,  -- This gives the file name back 
    status TEXT NOT NULL DEFAULT 'uploaded' -- This returns the uploaded status
)