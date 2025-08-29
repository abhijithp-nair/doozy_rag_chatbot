import os
import faiss
import pickle
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Global embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# PDF loader
def load_pdfs(pdf_path="data.pdf"):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} not found!")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Chunk text
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Build or load FAISS
def build_or_load_index(chunks, index_file="faiss_index.pkl"):
    if os.path.exists(index_file):
        with open(index_file, "rb") as f:
            index, stored_chunks = pickle.load(f)
        return index, stored_chunks

    embeddings = embedding_model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    with open(index_file, "wb") as f:
        pickle.dump((index, chunks), f)

    return index, chunks

# Retrieve
def retrieve_relevant_chunks(query, index, chunks, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

# Ask Ollama
def ask_ollama(query, context, model="gemma:2b"):
    prompt = f"You are Doozy, a helpful chatbot. Use the following context to answer:\n\n{context}\n\nQuestion: {query}\nAnswer as Doozy:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        return f"[Error contacting Ollama: {e}]"

# Main answer
def answer_query(query, index, chunks, model="gemma:2b"):
    relevant_chunks = retrieve_relevant_chunks(query, index, chunks)
    context = "\n".join(relevant_chunks)
    return ask_ollama(query, context, model=model)

# Scrape website + update FAISS
def scrape_website_and_update_index(url, index, stored_chunks, chunk_size=500, overlap=50):
    try:
        print(f"[scrape] Fetching {url}...")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Get clean text
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=" ", strip=True)

        # Chunk & embed
        new_chunks = chunk_text(text, chunk_size, overlap)
        embeddings = embedding_model.encode(new_chunks)
        index.add(embeddings)
        stored_chunks.extend(new_chunks)

        return f"✅ Scraped and added content from {url}"
    except Exception as e:
        return f"❌ Failed to scrape {url}: {e}"
