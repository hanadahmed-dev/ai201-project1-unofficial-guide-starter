from pathlib import Path
import re
import html
import json

# Configuration from planning.md
CHUNK_SIZE = 400
OVERLAP = 75

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")


def load_documents():
    documents = []

    for file_path in RAW_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


def clean_text(text):
    # Remove HTML entities
    text = html.unescape(text)

    # Remove HTML tags if any exist
    text = re.sub(r"<[^>]+>", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += (chunk_size - overlap)

    return chunks


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    documents = load_documents()

    print(f"\nLoaded documents: {len(documents)}\n")

    all_chunks = []

    for doc in documents:

        cleaned_text = clean_text(doc["text"])

        chunks = chunk_text(cleaned_text)

        print(f"{doc['filename']} -> {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["filename"],
                "chunk_id": i,
                "text": chunk
            })

    print("\n" + "=" * 80)
    print("SAMPLE CHUNKS")
    print("=" * 80)

    for chunk in all_chunks[:5]:
        print(f"\nSOURCE: {chunk['source']}")
        print(f"CHUNK: {chunk['chunk_id']}")
        print("-" * 40)
        print(chunk["text"])
        print("-" * 40)

    print("\n" + "=" * 80)
    print(f"TOTAL CHUNKS: {len(all_chunks)}")
    print("=" * 80)

    output_file = OUTPUT_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nSaved chunks to: {output_file}")


if __name__ == "__main__":
    main()