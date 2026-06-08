import os
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, build_chunks

COLLECTION_NAME = "tempe_housing"
CHROMA_DIR = "chroma_store"
TOP_K = 5

# load embedding model
print("Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")


def get_collection():
    """Return ChromaDB collection, creating it if needed."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def embed_and_store(chunks):
    """Embed all chunks and store in ChromaDB with metadata."""
    collection = get_collection()

    # skip if already populated
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} chunks. Skipping embed step.")
        print("(Delete the chroma_store/ folder to re-embed from scratch.)")
        return collection

    print(f"Embedding {len(chunks)} chunks...")
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    chunk_indexes = [str(c["chunk_index"]) for c in chunks]
    ids = [f"{c['source']}__chunk{c['chunk_index']}" for c in chunks]

    # embed in batches of 64
    batch_size = 64
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.extend(embeddings.tolist())
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} chunks...")

    collection.add(
        ids=ids,
        embeddings=all_embeddings,
        documents=texts,
        metadatas=[
            {"source": s, "chunk_index": ci}
            for s, ci in zip(sources, chunk_indexes)
        ]
    )
    print(f"Stored {collection.count()} chunks in ChromaDB.")
    return collection


def retrieve(query, k=TOP_K):
    """Retrieve top-k most relevant chunks for a query."""
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 4)
        })
    return chunks


def test_retrieval():
    """Test retrieval with 3 of our 5 evaluation questions."""
    test_queries = [
        "What do students say about maintenance at Skye at McClintock Station?",
        "What are the cheapest apartment options near ASU Tempe?",
        "Are there any reports of mold or pest problems in Tempe apartments?",
    ]

    print("\n" + "="*60)
    print("RETRIEVAL TEST")
    print("="*60)

    for query in test_queries:
        print(f"\nQUERY: {query}")
        print("-" * 50)
        results = retrieve(query)
        for i, chunk in enumerate(results, 1):
            print(f"\n  Result {i} | Source: {chunk['source']} | Distance: {chunk['distance']}")
            print(f"  {chunk['text'][:200]}...")
        print()


if __name__ == "__main__":
    # load and chunk documents
    print("Loading documents...")
    documents = load_documents("documents")
    chunks = build_chunks(documents)
    print(f"Total chunks: {len(chunks)}")

    # embed and store
    collection = embed_and_store(chunks)

    # test retrieval
    test_retrieval()