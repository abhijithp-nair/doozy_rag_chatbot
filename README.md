Doozy RAG Chatbot

Doozy is a Retrieval-Augmented Generation (RAG) chatbot designed to enable interactive conversations with both static documents (PDF) and dynamically scraped website content.
It leverages FAISS for vector search, SentenceTransformers for semantic embeddings, and the Gemma model (served locally via Ollama) as the language generation backend.

Project Architecture
doozy_rag_chatbot/
│── run.py                 # Main entry point (CLI + Gradio UI)
│── rag_core.py            # Core RAG logic (PDF ingestion, embeddings, web scraping, query answering)
│── requirements.txt       # Python dependencies
│── data.pdf               # Input PDF (default document for interaction)
│── README.md              # Project documentation

System Workflow
1. PDF Ingestion

rag_core.py loads and extracts text from data.pdf.

Extracted text is split into manageable chunks for downstream processing.

2. Indexing

Each text chunk is embedded using SentenceTransformer (all-MiniLM-L6-v2).

A FAISS vector index is created to enable efficient semantic search.

3. Query Handling

When a user submits a query, the system retrieves the most relevant chunks from the FAISS index.

Retrieved context is appended to the user’s question.

4. Response Generation

The enriched query is passed to Gemma (via Ollama).

The model generates a contextual response, consistently introducing itself as Doozy.

5. Web Scraping Extension

Users may supply a URL directly inside the chat.

The system scrapes the website content (using BeautifulSoup or Playwright), processes it into chunks, embeds it, and extends the FAISS index dynamically.

Subsequent responses integrate knowledge from both the PDF and scraped web sources.

Tech Stack

FAISS – Vector similarity search

SentenceTransformers – Embeddings (all-MiniLM-L6-v2)

Ollama – Local LLM serving

Gemma – Language model used for generation

Gradio – Web-based user interface

BeautifulSoup / Playwright – Web scraping utilities

Python 3.10+ – Core programming language

Setup Instructions
1. Clone the Repository

2. Create a Virtual Environment
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Install and Run Ollama

Download Ollama: https://ollama.com/download

Start the Ollama service:

ollama serve


Pull the Gemma model:

ollama pull gemma:2b

Running the Chatbot
Option 1: Command Line Interface (CLI)
python run.py

Option 2: Gradio Web UI
python run.py --ui


Launches a browser interface titled Doozy Chatbot.

Enables direct interaction with both document and web content.

Web Scraping Usage

To scrape a website during a session, type:

scrape https://example.com


The chatbot will ingest and index the site content. Future responses will combine knowledge from the PDF and the scraped web sources.

Deliverables

run.py – Main entry point (CLI and UI).

rag_core.py – Core RAG and scraping logic.

requirements.txt – Dependency list.

README.md – Documentation.

data.pdf – Default input document.

Notes

The chatbot always introduces and refers to itself as Doozy.

On first execution, the FAISS index is automatically created and reused on subsequent runs.

The system is modular, allowing extensions to additional data sources if required.