import gradio as gr
from query import ask


def handle_query(question):
    """Handle a user query and return answer + sources."""
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


# build Gradio UI
with gr.Blocks(title="ASU Tempe Housing Guide") as demo:
    gr.Markdown("""
    # 🏠 ASU Tempe Off-Campus Housing Guide
    ### The Unofficial Guide — powered by real student reviews and Reddit discussions
    Ask anything about off-campus housing near ASU Tempe: apartment quality, pricing, maintenance, safety, and more.
    """)

    with gr.Row():
        with gr.Column(scale=4):
            inp = gr.Textbox(
                label="Your Question",
                placeholder="e.g. What do students say about Skye at McClintock? Are there cheap apartments near ASU?",
                lines=2
            )
        with gr.Column(scale=1):
            btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(
            label="Answer",
            lines=10,
            interactive=False
        )

    with gr.Row():
        sources = gr.Textbox(
            label="Retrieved from these sources",
            lines=4,
            interactive=False
        )

    gr.Markdown("""
    ---
    **Example questions to try:**
    - What do students say about maintenance at Skye at McClintock Station?
    - Is Agave Apartments walkable to ASU campus?
    - What are the cheapest apartment options near ASU Tempe?
    - Do students recommend living off campus instead of ASU dorms?
    - Are there any reports of mold or pest problems in Tempe apartments?
    """)

    # wire up interactions
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()