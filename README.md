# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     This project covers student reviews and experiences with UC San Diego Computer Science professors. This knowledge is valuable because students often want information about teaching style, workload, exam difficulty, grading policies, and course organization before enrolling in a course. Official course catalogs and university websites provide course descriptions but do not capture the day-to-day student experience. Student reviews provide insight into factors such as lecture quality, assignment difficulty, professor accessibility, and overall course satisfaction.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
400 characters
**Overlap:**
75 characters
**Why these choices fit your documents:**
The documents consist primarily of short professor reviews and summaries rather than long articles. A chunk size of 400 characters was large enough to preserve meaningful review content while still allowing retrieval to focus on specific topics such as exams, workload, or teaching style. An overlap of 75 characters was used to reduce the chance of important information being lost at chunk boundaries.

Before chunking, documents were cleaned by removing excess whitespace and normalizing text formatting. The documents were then split into overlapping character-based chunks.
**Final chunk count:**
89 chunks across 10 professor documents.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 from Sentence Transformers
**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it is lightweight, runs locally, and does not require API calls or usage fees. For a production system, I would evaluate larger embedding models that may provide stronger semantic understanding and better retrieval accuracy. I would also consider support for multilingual reviews, longer context windows, and the tradeoff between retrieval quality and inference latency. Larger hosted models may improve accuracy but would increase cost and response time.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The LLM was instructed to answer only using the retrieved context. The prompt included the instruction:

"Use ONLY the provided context. Do not use outside knowledge. If the context does not contain enough information to answer, say 'I don't have enough information in the provided documents to answer that.'"

This instruction was included with every query before sending it to the LLM.
**How source attribution is surfaced in the response:**
Retrieved source filenames are collected programmatically from the retrieval step and displayed alongside the generated answer. This ensures source attribution is shown even if the language model does not explicitly cite sources in its generated response.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor is most frequently described as caring and supportive?| Sicun Gao | Retrieved multiple Sicun Gao reviews describing him as caring, supportive, accessible, and helpful. | Relevant | Accurate |
| 2 | Which professor receives the most positive feedback about teaching quality?| Sicun Gao | The system compared Sicun Gao and Ivonne Gonzalez Gamboa and concluded that Sicun Gao received the strongest overall teaching feedback based on ratings and reviews. | Relevant | Accurate |
| 3 | Which professor is associated with the heaviest workload? | Russell Impagliazzo | The system identified Russell Impagliazzo because reviews mentioned spending approximately 20 hours per week on homework and significant assignment effort. | Relevant | Accurate |
| 4 | Which professor is considered most beginner-friendly? | Ivonne Gonzalez Gamboa | The system identified Ivonne Gonzalez Gamboa because her course had the lowest reported difficulty and reviews described it as relatively easy and approachable. | Relevant | Accurate |
| 5 | Which professor has the most difficult exams? | Russell Impagliazzo, Edwin Solares, or Jor-El Briones | The system declined to answer because the retrieved context did not contain enough information to confidently compare exam difficulty across professors. | Partially relevant| Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor has the most difficult exams?
**What the system returned:**
The system declined to answer and stated that it did not have enough information in the retrieved documents to determine which professor had the most difficult exams.
**Root cause (tied to a specific pipeline stage):**
The failure occurred during retrieval. The embedding model retrieved chunks containing general difficulty information, quizzes, and course metadata rather than chunks specifically focused on exam difficulty. Because the chunks contained both review summaries and metadata, the retrieval stage was unable to consistently identify the strongest evidence needed for a direct comparison.
**What you would change to fix it:**
I would improve chunking by separating review metadata from review content and experiment with larger chunks that preserve more context. I would also consider hybrid retrieval that combines embeddings with keyword matching for terms such as "exam," "midterm," "final," and "test heavy."
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document helped guide the implementation by forcing me to define the domain, document sources, chunking strategy, and retrieval approach before writing code. Having these decisions documented made it easier to build the pipeline incrementally and verify that each milestone matched the intended architecture.
**One way your implementation diverged from the spec, and why:**
The original plan focused on collecting review information directly from online sources. During implementation, I instead converted the reviews into structured text documents before processing them. This approach simplified ingestion, avoided issues with scraping dynamic websites, and allowed me to focus on retrieval and generation rather than web scraping challenges.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
My chunking strategy, document structure, and Milestone 3 requirements.
- *What it produced:*
ChromaDB retrieval code using all-MiniLM-L6-v2 embeddings along with source metadata storage and semantic search functionality.
- *What I changed or overrode:*
I adjusted chunking parameters, inspected the generated chunks manually, and evaluated whether the chunks preserved enough context for retrieval.

**Instance 2**

- *What I gave the AI:*
My retrieval architecture, embedding model choice, and Milestone 4 requirements.
- *What it produced:*
ChromaDB retrieval code using all-MiniLM-L6-v2 embeddings along with source metadata storage and semantic search functionality.
- *What I changed or overrode:*
I modified the evaluation queries, tested retrieval quality manually, and analyzed retrieval failures to determine where the embedding model and chunking strategy could be improved.