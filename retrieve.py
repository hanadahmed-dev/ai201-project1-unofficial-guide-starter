import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_PATH = Path("data/processed/chunks.json")
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "professor_reviews"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store():
    chunks = load_chunks()

    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Reset collection so rerunning the script does not duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [f'{chunk["source"]}_{chunk["chunk_id"]}' for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"Saved {len(texts)} chunks to ChromaDB.")
    return collection, model


def load_vector_store():
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    return collection, model


def retrieve(query, k=4):
    collection, model = load_vector_store()

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    print("\nQUERY:")
    print(query)
    print("\nRESULTS:")
    print("=" * 80)

    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print(f"\nResult {i + 1}")
        print(f"Source: {metadata['source']}")
        print(f"Chunk ID: {metadata['chunk_id']}")
        print(f"Distance: {distance:.4f}")
        print("-" * 40)
        print(doc)
        print("-" * 40)


if __name__ == "__main__":
    build_vector_store()

    test_queries = [
        "Which professor has exams that are harder than lectures or homework?",
        "Which professor is described as caring, supportive, and accessible outside class?",
        "Which professor has time consuming homework and programming assignments?",
    ]

    for query in test_queries:
        retrieve(query, k=4)