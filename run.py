import argparse
import gradio as gr
from rag_core import (
    load_pdfs, chunk_text, build_or_load_index,
    answer_query, scrape_website_and_update_index
)

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--ui", action="store_true", help="Launch Gradio UI")
args = parser.parse_args()

# Load PDF & build FAISS index
print("[pdf] Loading PDF...")
text = load_pdfs("data.pdf")
chunks = chunk_text(text)
print("[index] Building / Loading FAISS index...")
index, stored_chunks = build_or_load_index(chunks)

# Response function
def respond(message, history):
    if message.lower().startswith("scrape "):
        url = message.split(" ", 1)[1].strip()
        reply = scrape_website_and_update_index(url, index, stored_chunks)
    else:
        reply = answer_query(message, index, stored_chunks, model="gemma:2b")

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return history

# Gradio UI
if args.ui:
    with gr.Blocks(title="Doozy Chatbot") as demo:
        gr.Markdown("## 🤖 Doozy Chatbot\nChat with your PDF + scraped websites!")
        chatbot = gr.Chatbot(label="Doozy", type="messages")
        msg = gr.Textbox(label="Ask Doozy anything...")
        msg.submit(respond, [msg, chatbot], chatbot)
    demo.launch(share=True)
else:
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        if q.lower().startswith("scrape "):
            url = q.split(" ", 1)[1].strip()
            print("Doozy:", scrape_website_and_update_index(url, index, stored_chunks))
        else:
            print("Doozy:", answer_query(q, index, stored_chunks, model="gemma:2b"))
