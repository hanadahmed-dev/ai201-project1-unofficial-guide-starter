import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join(f"• {source}" for source in result["sources"])

    retrieved_chunks = "\n\n".join(
        f"Source: {chunk['source']} | Chunk ID: {chunk['chunk_id']} | Distance: {chunk['distance']:.4f}\n"
        f"{chunk['text']}"
        for chunk in result["chunks"]
    )

    return result["answer"], sources, retrieved_chunks


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide: UCSD Professor Reviews")
    gr.Markdown("Ask a question about the professor review documents.")

    question = gr.Textbox(label="Your question", placeholder="Which professor is caring and supportive?")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)
    chunks = gr.Textbox(label="Retrieved chunks", lines=12)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources, chunks])
    question.submit(handle_query, inputs=question, outputs=[answer, sources, chunks])


demo.launch()