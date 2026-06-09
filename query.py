import os
from dotenv import load_dotenv
from groq import Groq

from retrieve import load_vector_store


load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def retrieve_chunks(question, k=4):
    collection, embedding_model = load_vector_store()
    query_embedding = embedding_model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": results["distances"][0][i],
        })

    return chunks


def build_context(chunks):
    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f'Source: {chunk["source"]}, Chunk ID: {chunk["chunk_id"]}\n'
            f'{chunk["text"]}'
        )

    return "\n\n---\n\n".join(context_parts)


def ask(question):
    chunks = retrieve_chunks(question, k=4)
    context = build_context(chunks)

    source_names = sorted(set(chunk["source"] for chunk in chunks))

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are answering questions about UCSD professor reviews.

Use ONLY the provided context.
Do not use outside knowledge.
If the context does not contain enough information to answer, say:
"I don't have enough information in the provided documents to answer that."

Always mention the professor names and cite the source filenames.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a grounded RAG assistant. Answer only using retrieved context.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": source_names,
        "chunks": chunks,
    }


if __name__ == "__main__":
    result = ask("Which professor teaches quantum mechanics?")
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print("-", source)