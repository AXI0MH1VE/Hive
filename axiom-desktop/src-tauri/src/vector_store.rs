use rusqlite::{Connection, Result};
use sqlite_vec::sqlite3_vec_init;
use std::path::Path;

pub struct VectorStore {
    conn: Connection,
}

impl VectorStore {
    pub fn new(db_path: &str) -> Result<Self> {
        let conn = Connection::open(Path::new(db_path))?;
        
        // Initialize sqlite-vec
        sqlite3_vec_init(&conn)?;
        
        // Create table for vectors
        conn.execute(
            "CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY,
                data TEXT,
                embedding BLOB
            )",
            [],
        )?;
        
        // Create vector index
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS vec_items USING vec0(
                embedding float[384]  /* Adjust dimension based on model */
            )",
            [],
        )?;
        
        Ok(Self { conn })
    }
    
    pub fn insert(&self, data: &str, embedding: &[f32]) -> Result<()> {
        let embedding_bytes = bytemuck::cast_slice(embedding);
        
        self.conn.execute(
            "INSERT INTO vectors (data, embedding) VALUES (?1, ?2)",
            [data, &embedding_bytes],
        )?;
        
        // Insert into vector table
        self.conn.execute(
            "INSERT INTO vec_items (embedding) VALUES (?1)",
            [&embedding_bytes],
        )?;
        
        Ok(())
    }
    
    pub fn search(&self, query_embedding: &[f32], limit: usize) -> Result<Vec<String>> {
        let query_bytes = bytemuck::cast_slice(query_embedding);
        
        let mut stmt = self.conn.prepare(
            "SELECT v.data FROM vec_items vi
             JOIN vectors v ON vi.rowid = v.rowid
             ORDER BY distance(vi.embedding, ?1)
             LIMIT ?2",
        )?;
        
        let rows = stmt.query_map([query_bytes, &limit.to_string()], |row| row.get(0))?;
        
        let mut results = Vec::new();
        for row in rows {
            results.push(row?);
        }
        
        Ok(results)
    }
}