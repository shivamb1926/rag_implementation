import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

def load_embeddings():
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, text, source, embedding FROM documents")
    rows = cursor.fetchall()
    
    data = []
    
    for row in rows:
        embedding = np.frombuffer(row[3], dtype=np.float32)
        
        data.append({
            "id": row[0],
            "text": row[1],
            "source": row[2],
            "embedding": embedding
        })
    
    conn.close()
    
    return data

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


model = SentenceTransformer("all-MiniLM-L6-v2")

stored_data = load_embeddings()

def retrieve(query, k=7):
    query_embedding = model.encode([query])[0]
    
    similarities = []
    
    for item in stored_data:
        sim = cosine_similarity(query_embedding, item["embedding"])
        similarities.append((sim, item))
    
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    return [item for _, item in similarities[:k]]