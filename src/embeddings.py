from sentence_transformers import SentenceTransformer


def create_embeddings(all_chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings

