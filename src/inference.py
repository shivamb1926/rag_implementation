import requests
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def generate(prompt, model="phi3"):
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        response.raise_for_status()
        return response.json().get("response", "")
    
    except Exception as e:
        return f"Error: {str(e)}"