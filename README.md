Doozy RAG Chatbot: 

Doozy is a Retrieval-Augmented Generation (RAG) chatbot that allows you to interact with the contents of a PDF document and dynamically scraped websites.
It is powered by FAISS for semantic search, SentenceTransformers for embeddings, and Gemma (via Ollama) as the local LLM backend.

📂 Project Architecture
doozy_rag_chatbot/
│── run.py                 # Main entry point (CLI + Gradio UI)
│── rag_core.py            # Core RAG logic (PDF loading, embeddings, web scraping, query answering)
│── requirements.txt       # Dependencies
│── data.pdf               # Input PDF (document to chat with)
│── faiss_index.pkl        # Auto-created FAISS index (on first run)
│── README.md              # Documentation

Code Flow: 

PDF Ingestion

rag_core.py → load_pdfs() extracts text from data.pdf.

Text is chunked into manageable pieces (chunk_text()).

Indexing:

Each chunk is converted into embeddings using SentenceTransformer (all-MiniLM-L6-v2).

A FAISS vector index is built (or loaded if already created).

Query Handling:

When the user asks a question, the system retrieves the most relevant chunks from the PDF/web content.

Context is appended to the user query.

LLM Response:

The context-enriched query is sent to Ollama (Gemma model).

The model generates the response as Doozy.

Web Scraping Extension:

Users can input a URL inside the chat.

The system scrapes website text (BeautifulSoup/Playwright), chunks & embeds it, and extends the FAISS index dynamically.

Doozy can now answer questions from both the PDF and scraped sites.


 Setup Instructions:
1. Clone the Repository
git clone https://github.com/<your-username>/doozy_rag_chatbot.git
cd doozy_rag_chatbot

2. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)

3. Install Dependencies
pip install -r requirements.txt

4. Install & Run Ollama

Download Ollama from https://ollama.com/download

Start Ollama service:

ollama serve


Pull the Gemma model:

ollama pull gemma:2b

Running the Chatbot
Option 1: Command Line Interface (CLI)
python run.py

Option 2: Gradio Web UI
python run.py --ui


Opens a browser window titled "Doozy Chatbot".

Chat directly with the document and scraped websites.

 Web Scraping Feature

Inside the chat, type:

scrape https://example.com


The chatbot will scrape the site, add it to FAISS, and use both PDF + Web content for future answers.

Deliverables

1. run.py → Main entry point (UI + CLI).

2. rag_core.py → RAG + scraping logic.

3. requirements.txt → Dependencies.

4. README.md → Documentation.

5. data.pdf → Document to chat with.

Note:
The chatbot always introduces itself as Doozy and refers to itself consistently throughout conversations.