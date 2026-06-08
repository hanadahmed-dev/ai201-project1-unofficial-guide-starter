# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Student reviews and experiences with UCSD Computer Science professors.

This knowledge is valuable because students often want information about teaching style, workload, exam difficulty, grading policies, and course organization before enrolling. Official course catalogs provide basic course descriptions, but detailed information about the student experience is usually found in review sites and online discussions.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | RateMyProfessor| Russell Impagliazzo| https://www.ratemyprofessors.com/professor/563826 |
| 2 | RateMyProfessor| Janine Tiefenbruck| https://www.ratemyprofessors.com/professor/1992606 |
| 3 | RateMyProfessor | Sicun Gao| https://www.ratemyprofessors.com/professor/2342149 
| 4 | RateMyProfessor | Jor-El Briones | https://www.ratemyprofessors.com/professor/2873547 |
| 5 | RateMyProfessor | Yingjun Cao | https://www.ratemyprofessors.com/professor/2046827 |
| 6 | RateMyProfessor | Bryan Chin | https://www.ratemyprofessors.com/professor/2345822 |
| 7 | RateMyProfessor | Ivonne Gonzalez Gamboa | https://www.ratemyprofessors.com/professor/2987363 |
| 8 | RateMyProfessor | Paul Cao | https://www.ratemyprofessors.com/professor/2772323 |
| 9 | RateMyProfessor | Thomas Powell | https://www.ratemyprofessors.com/professor/857885 |
| 10 | RateMyProfessor | Edwin Solares | https://www.ratemyprofessors.com/professor/2999053 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

400 characters

**Overlap:**

75 characters

**Reasoning:**

My documents consist primarily of short student reviews rather than long-form articles. A chunk size of 400 characters is large enough to preserve complete opinions about teaching style, workload, exams, and grading policies while remaining focused on a single topic. A 75-character overlap helps preserve context when an important review spans multiple chunks and reduces the chance of splitting meaningful information across chunk boundaries.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

all-MiniLM-L6-v2 from sentence-transformers

**Top-k:**

4

**Production tradeoff reflection:**

I chose all-MiniLM-L6-v2 because it is free, runs locally, and performs well for semantic search tasks. If this system were deployed in production, I would evaluate larger embedding models that may provide better retrieval accuracy, support multilingual reviews, and handle more domain-specific language. However, these improvements would come with increased cost, latency, and infrastructure requirements.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which professor is most frequently described as having difficult exams? | The professor whose reviews most consistently mention difficult exams. |
| 2 | Which professor is considered the most beginner-friendly? | The professor whose reviews frequently mention clear explanations and accessibility for new students. |
| 3 | Which professor receives the most positive feedback about teaching quality? | The professor with the highest concentration of positive teaching-related reviews. |
| 4 | Which professor provides the most helpful office hours or feedback? | The professor whose reviews frequently mention useful office hours or detailed feedback.  |
| 5 | Which professor is associated with the heaviest workload? | The professor whose reviews most frequently mention time-consuming assignments or heavy workloads. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Student reviews may contain conflicting opinions, making it difficult to determine a single correct answer.

2. Retrieval may return reviews that contain similar language but discuss different topics, reducing answer accuracy.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     RateMyProfessor Reviews
          ↓
     Document Ingestion (Python)
          ↓
     Chunking (Custom Chunker)
          ↓
     Embeddings (all-MiniLM-L6-v2)
          ↓
     ChromaDB Vector Store
          ↓
     Semantic Retrieval (Top-4)
          ↓
     Groq Llama 3.3
          ↓
     Grounded Response + Sources

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will use ChatGPT to help implement the document ingestion and chunking pipeline. I will provide my Documents section, Chunking Strategy section, and Architecture diagram as input. I will ask ChatGPT to generate Python code that loads my professor review documents, cleans the text, and splits it into chunks using my specified chunk size of 400 characters and overlap of 75 characters. I will verify the implementation by printing sample chunks and checking that they contain complete thoughts and match my chunking specification.

**Milestone 4 — Embedding and retrieval:**

I will use ChatGPT to help implement the embedding and retrieval components. I will provide my Retrieval Approach section and Architecture diagram as input. I will ask ChatGPT to generate code that uses the all-MiniLM-L6-v2 embedding model, stores embeddings in ChromaDB, and retrieves the top 4 most relevant chunks for a query. I will verify the implementation by running test queries and checking that the returned chunks are relevant to the questions being asked.

**Milestone 5 — Generation and interface:**

I will use ChatGPT to help implement the response generation and Gradio interface. I will provide my Architecture diagram, Retrieval Approach section, and project requirements. I will ask ChatGPT to generate code that sends retrieved chunks to the Groq Llama model, produces grounded responses, and displays answers with source citations in a Gradio interface. I will verify the implementation by confirming that responses are based only on retrieved documents, include source attribution, and correctly refuse to answer questions not covered by the documents.
