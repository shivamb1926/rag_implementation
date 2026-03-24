from src.retrieve import retrieve
from src.inference import generate

def build_context(results):
    context = ""
    
    for i, r in enumerate(results):
        context += f"[Chunk {i+1} | Source: {r['source']}]\n"
        context += r["text"] + "\n\n"
    
    return context

def build_prompt(query, context):
    return f"""
You are a helpful assistant.

Answer the question ONLY using the context below.
If the answer is not in the context, say "I don't know".

Keep the answer concise (3-4 sentences).

Context:
{context}

Question:
{query}

Answer:
"""

def extract_sources(results):
    return list(set([r["source"] for r in results]))

def ask(query):
    results = retrieve(query, k=5)
    
    context = build_context(results)
    
    # context = context[:2000]
    
    prompt = build_prompt(query, context)
    
    response = generate(prompt)
    
    sources = extract_sources(results)
    
    return {
        "answer": response.strip(),
        "sources": sources
    }