CREATE EXTENSION IF NOT EXISTS vector; -- Creating the vector extension if it doesnot EXISTS

-- Creating the table to add the information of the chunks 
CREATE table chunks (
    id TEXT PRIMARY KEY, -- each vector unique id 
    file_id TEXT NOT NULL,  -- common file id belongs to the same id
    chunk_index INT NOT NULL, --ordering chunks basedon the file_id
    chunks TEXT NOT NULL,  -- Raw generated chunks
    embedding vector(384) NOT NULL, --Embedded chunks to vectors
    UNIQUE (file_id, chunk_index) -- file id and chunkindex needs to be unique
);

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops); -- The Hierarchical Navigable Small World (HNSW) is a way to search the vectors with the highest cosine similarity in the dense vector database 