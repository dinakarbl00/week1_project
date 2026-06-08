import os
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def build_prompt(query, chunks):
    """Build a grounded prompt using only retrieved chunks as context."""
    context_blocks = []
    for i, chunk in enumerate(chunks, 1):
        context_blocks.append(f"[Source {i}: {chunk['source']}]\n{chunk['text']}")
    context = "\n\n".join(context_blocks)

    system_prompt = """You are a helpful assistant that answers questions about off-campus housing near ASU Tempe.

CRITICAL RULES:
1. Answer ONLY using the information provided in the sources below.
2. Do NOT use any outside knowledge or make assumptions beyond what is in the sources.
3. Always cite which source(s) your answer draws from (e.g. "According to skye_mclintock_google_reviews.txt...").
4. If the provided sources do not contain enough information to answer the question, respond with exactly: "I don't have enough information in my documents to answer that question."
5. Do not make up apartment names, prices, or experiences that are not mentioned in the sources."""

    user_prompt = f"""Here are the relevant documents retrieved for this question:

{context}

Question: {query}

Answer based only on the sources above, and cite which source(s) you used."""

    return system_prompt, user_prompt


def ask(query):
    """Full RAG pipeline: retrieve chunks, generate grounded answer."""
    # retrieve relevant chunks
    chunks = retrieve(query)

    # build grounded prompt
    system_prompt, user_prompt = build_prompt(query, chunks)

    # generate answer
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    # collect unique sources
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    # quick test
    test_queries = [
        "What do students say about maintenance at Skye at McClintock Station?",
        "What is the best time to visit the moon?",  # out of scope test
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print(f"{'='*60}")
        result = ask(query)
        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {result['sources']}")