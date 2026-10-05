CREATE EXTENSION IF NOT EXISTS vector; -- Creating the vector extension if it doesnot EXISTS

-- Creating the table to add the information of the chunks 
CREATE table chunks (
    id TEXT PRIMARY KEY, 
    file_id TEXT NOT NULL, 
    chunk_index INT NOT NULL, 
    chunks TEXT NOT NULL, 
    embedding vector(384) NOT NULL, 
    UNIQUE (file_id, chunk_index)
)