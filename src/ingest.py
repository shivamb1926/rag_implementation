import sqlite3
import numpy as np
from load_docs import load_markdown_files, chunk_text
from embeddings import create_embeddings

def setup_database():
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        source TEXT,
        embedding BLOB
    )
    """)

    conn.commit()

def serialize_embedding(embedding):
    return embedding.astype(np.float32).tobytes()

def ingest():
    setup_database()

    docs = load_markdown_files()

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["content"])
        
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": doc["filename"]
            })

    embeddings = create_embeddings(all_chunks)


    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    for chunk, emb in zip(all_chunks, embeddings):
        cursor.execute("""
        INSERT INTO documents (text, source, embedding)
        VALUES (?, ?, ?)
        """, (
            chunk["text"],
            chunk["source"],
            serialize_embedding(emb)
        ))

    conn.commit()
    



if __name__ == "__main__":
    ingest()