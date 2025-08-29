# Doozy — Local RAG Chatbot (PDF + Web Scraping)

Doozy is a local Retrieval-Augmented Generation (RAG) chatbot that can chat over PDF documents and scraped webpages.
It is designed for **local LLMs** served via **Ollama**, but you can easily swap to other local servers if you prefer.

> The chatbot always introduces and refers to itself as **"Doozy"**.

---

## ✨ Features
- 🔎 Ingest one or more PDFs — automatically chunked & embedded locally.
- 🌐 Scrape one or more URLs (BeautifulSoup) — merge with PDF knowledge base.
- 🧠 Fast vector search with FAISS.
- 🤖 Talk to a **local** LLM via **Ollama** (`/api/chat` & `/api/embeddings`).
- 💬 CLI chat *or* simple Gradio UI (`--ui gradio`).
- 💾 On-disk persistence in `./storage` so you can reuse the index later.
- 🔐 No external APIs required.

---

## 🧱 Architecture
```
run.py                # Entry point (CLI or Gradio UI)
rag_core.py           # RAG pipeline: chunking, embeddings, indexing, retrieval, generation
loaders.py            # PDF loader and text cleaners
web_scrape.py         # URL scraping (requests + BeautifulSoup)
requirements.txt      # Python deps
README.md             # This file
storage/              # (auto) FAISS index + chunk metadata
```

---

## ✅ Requirements
- Python 3.9+
- [Ollama](https://ollama.com) running locally at `http://localhost:11434`  
  Pull the models (or let Ollama pull them on first use):
  ```bash
  ollama pull llama3.1:8b-instruct
  ollama pull nomic-embed-text
  ```

> You can switch to other local models by changing CLI flags.

---

## 🚀 Quickstart

### 1) Install Python deps
```bash
pip install -r requirements.txt
```

### 2) Start Ollama (if not already)
```bash
ollama serve
```

### 3) Run with PDFs
```bash
python run.py --pdfs path/to/file1.pdf path/to/file2.pdf
```

### 4) Also scrape URLs
```bash
python run.py --pdfs path/to/file.pdf --urls https://example.com https://docs.example.org
```

### 5) Use the Gradio UI
```bash
python run.py --pdfs path/to/file.pdf --ui gradio
```

### 6) Reuse existing index
```bash
python run.py --reuse-index
```

---

## 🔧 Common Flags
```bash
python run.py   --pdfs path/to/a.pdf path/to/b.pdf   --urls https://example.com   --ollama-model llama3.1:8b-instruct   --embed-model nomic-embed-text   --chunk-size 800   --chunk-overlap 150   --k 5   --ui cli
```

---

## 🧪 Example Prompts
- "Summarize the attached PDF."
- "From the website, list the three most important recommendations."
- "Compare the PDF section on security with this URL's security page."

---

## 🔒 Notes
- This system is **local-first** and uses **no external cloud APIs**.
- If your target site is JavaScript-heavy, you can extend `web_scrape.py` to Playwright easily.
- The FAISS index and metadata are written to `./storage/` by default.

---

## 📦 Submission
This repository already matches the requested structure:
- `run.py` — primary entry point
- `requirements.txt` — dependencies
- Additional helper modules under the same root.

Push to a public GitHub repo and you're done. Good luck! ✨
