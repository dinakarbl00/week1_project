import os
import random

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 400
OVERLAP = 80


def load_documents(folder_path):
    """Load all .txt files from the documents folder."""
    documents = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".txt") and filename != ".gitkeep":
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
                # remove SOURCE header line so URLs don't get embedded as chunks
                lines = text.split('\n')
                lines = [l for l in lines if not l.startswith('SOURCE:') and not l.startswith('source:')]
                text = '\n'.join(lines).strip()
            if text:
                documents.append({
                    "source": filename,
                    "text": text
                })
                print(f"  Loaded: {filename} ({len(text)} characters)")
    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split text into overlapping character-based chunks.
    Each chunk is chunk_size characters, with overlap characters
    of context carried over from the previous chunk.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # skip tiny leftover chunks
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_chunks(documents):
    """Chunk all documents and attach source metadata."""
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i
            })
    return all_chunks


def inspect_chunks(all_chunks, n=5):
    """Print n random chunks so we can verify quality."""
    print(f"\n{'='*60}")
    print(f"CHUNK INSPECTION — {n} random samples")
    print(f"{'='*60}")
    samples = random.sample(all_chunks, min(n, len(all_chunks)))
    for i, chunk in enumerate(samples, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Source : {chunk['source']}")
        print(f"Index  : {chunk['chunk_index']}")
        print(f"Length : {len(chunk['text'])} characters")
        print(f"Text   :\n{chunk['text']}")
    print(f"\n{'='*60}")


if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents(DOCUMENTS_DIR)
    print(f"\nLoaded {len(documents)} documents.")

    print("\nChunking documents...")
    all_chunks = build_chunks(documents)
    print(f"Total chunks produced: {len(all_chunks)}")

    inspect_chunks(all_chunks, n=5)

    # quick sanity check on chunk count
    if len(all_chunks) < 50:
        print("\nWARNING: fewer than 50 chunks — chunks may be too large.")
    elif len(all_chunks) > 2000:
        print("\nWARNING: more than 2000 chunks — chunks may be too small.")
    else:
        print(f"\nChunk count looks healthy ({len(all_chunks)} total).")