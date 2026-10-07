SELECT file_id, count(*) AS n_chunks, min(chunk_index), max(chunk_index)
FROM chunks GROUP BY file_id;