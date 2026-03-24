import os

def load_markdown_files():
    documents = []
    folder_path = "./data"

    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({
                    "filename": file,
                    "content": text
                })
    
    return documents

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    
    return chunks

if __name__ == "__main__":
    docs = load_markdown_files()