# Project 1 Planning: The Unofficial Guide

<!-- > Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features. -->

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This project covers **Tempe off-campus housing for ASU students**, specifically student-generated reviews, Reddit discussions, and tenant experiences about apartment complexes near ASU's Tempe campus.
 
This knowledge is valuable because official ASU housing pages only list affiliated complexes and say nothing about maintenance responsiveness, hidden fees, pest issues, or what it's actually like to live somewhere. A prospective student Googling "apartments near ASU" gets polished marketing pages. The real knowledge: cockroach problems at Agave, sewage smells at Skye, which complexes have predatory move-out charges, which ones are actually walkable to campus, it all lives in Reddit threads and Google Maps reviews that are hard to search systematically. This RAG system makes that scattered, informal knowledge answerable through plain-language questions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Google Maps — Agave Apartments | Tenant reviews of Agave Apartments, Tempe | https://www.google.com/maps/place/Agave/@33.409112,-111.9241147 |
| 2 | Google Maps — The Piedmont | Tenant reviews of The Piedmont by Mark-Taylor | https://www.google.com/maps/place/The+Piedmont/@33.4242746,-111.9281299 |
| 3 | Google Maps — Skye at McClintock Station | Tenant reviews of Skye at McClintock Station | https://www.google.com/maps/place/Skye+at+McClintock+Station/@33.4140004,-111.9065104 |
| 4 | Google Maps — Skywater at Tempe Town Lake | Tenant reviews of Skywater at Tempe Town Lake | https://www.google.com/maps/place/Skywater+at+Tempe+Town+Lake/@33.4303458,-111.9482323 |
| 5 | ApartmentRatings.com — IMT Desert Palm Village | Verified tenant reviews, maintenance and staff ratings | https://www.apartmentratings.com/az/tempe/imt-desert-palm-village_480968109985281/ |
| 6 | ApartmentRatings.com — Allure at Tempe | Verified tenant reviews for Allure at Tempe | https://www.apartmentratings.com/az/tempe/allure-at-tempe/ |
| 7 | r/ASU — "What apartments are good in Tempe near ASU?" | Student recommendations and personal experiences | https://www.reddit.com/r/ASU/comments/1np68lm/what_apartments_are_good_in_tempe_near_asu/ |
| 8 | r/ASU — "Cheap apartments near ASU Tempe recommendations?" | Budget-focused student housing discussion | https://www.reddit.com/r/ASU/comments/1d6osqa/cheap_apartments_near_asu_tempe_recommendations/ |
| 9 | r/ASU — "Off campus freshman year" | Discussion about pros/cons of off-campus living as a freshman | https://www.reddit.com/r/ASU/comments/19dtoqo/off_campus_freshman_year/ |
| 10 | r/ASU — "Is there a reason most students live off campus?" | Discussion about why students prefer off-campus housing over ASU dorms | https://www.reddit.com/r/ASU/comments/s1jwkv/is_there_a_reason_most_students_live_off_campus/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Reasoning:**
My documents has two types of text. Reviews from Google Maps and ApartmentRatings are short and opinionated, usually a few sentences about one thing, like maintenance or noise. Reddit threads run longer, but each reply is really just one person's take.

So I treat every review and every Reddit reply as its own retrievable unit. Chunk too small (say 100 characters) and a single thought gets sliced in half, leaving neither piece useful. Chunk too big (1000 characters) and you end up blending multiple views, often very different, into one embedding, which muddies the signal and tanks retrieval.

400 characters fits one review or reply while staying on a single topic. The 80-character overlap is just insurance.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 5

**Production tradeoff reflection:**
For this project, `all-MiniLM-L6-v2` is a practical choice — it runs locally with no API key or rate limits, has reasonable accuracy on short opinion text, and produces 384-dimensional embeddings that are fast to query in ChromaDB.

For a production deployment serving real students, I would weigh several tradeoffs:
 
- **Context length:** `all-MiniLM-L6-v2` truncates at 256 tokens. For longer Reddit threads, this means some chunk content gets silently dropped during embedding. A model like `text-embedding-3-small` (OpenAI) or `embed-english-v3.0` (Cohere) supports longer contexts and may produce better embeddings for multi-sentence chunks.
- **Accuracy on domain-specific text:** Student slang and apartment-specific terminology ("in-unit W/D", "UPass", "per-bed lease") may not be well-represented in a general-purpose model. A fine-tuned or larger model would handle this better.
- **Local vs. API-hosted:** Running locally avoids cost and latency from network calls but limits model size. For production with many concurrent users, an API-hosted embedding service with batching would be more scalable.
- **Multilingual support:** ASU has a large international student population. A multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` might surface relevant reviews written in other languages.

Top-k of 5 balances giving the LLM enough context to synthesize an answer while avoiding dilution from loosely related chunks. Too few (k=2) risks missing the most relevant review if retrieval isn't perfect; too many (k=10) risks flooding the prompt with off-topic content.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about maintenance at Skye at McClintock Station? | Reviews mention slow or unresponsive maintenance, dirty hallways, and sewage/flooding issues. Some positive experiences with specific staff members. |
| 2 | Is Agave Apartments walkable to ASU campus? | At least one review mentions it is walking distance to ASU. |
| 3 | What are the cheapest apartment options near ASU Tempe according to students? | Reddit mentions Alight Tempe (~$700-840/month with roommates), Yugo, and Metro 101 / The Access as budget options. |
| 4 | Do students recommend living off campus instead of ASU dorms? Why? | Yes — Reddit discussions cite cost (dorms ~$4k/semester vs ~$1100 off-campus), more freedom, in-unit amenities, and ASU's limited upper-division dorm availability. |
| 5 | Are there any reports of mold or pest problems in Tempe apartments near ASU? | Yes — cockroaches mentioned at Agave, mold at The Piedmont, sewage smell at Skye at McClintock, and a warning about Murietta at ASU (black mold, per Reddit). |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Truncated reviews ("… More"):** Many Google Maps and ApartmentRatings reviews were scraped with truncated text ending in "… More" because the full review requires a click to expand. This means some chunks will contain incomplete information, which could cause the system to return partial answers or miss key details. This is a known data quality limitation of the data in hand.

2. **Off-topic retrieval from Reddit threads:** Reddit threads drift — a thread about cheap apartments near ASU also contains parking permit advice, sublet offers, and jokes. These off-topic chunks share vocabulary with housing queries and may surface when they shouldn't. This could cause the LLM to include irrelevant information in responses, especially for broad queries.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                        PIPELINE                                 │
                    └─────────────────────────────────────────────────────────────────┘
                    
                    [1] Document Ingestion          [2] Chunking
                    ─────────────────────           ────────────────────
                    Tool: Python + plain .txt       Tool: custom chunk_text()
                    - Load 10 .txt files            - 400 char chunks
                    - Extract source URL            - 80 char overlap
                    - Strip residual noise          - attach source metadata
                         │                                │
                         └──────────────┬─────────────────┘
                                        ▼
                    [3] Embedding + Vector Store
                    ────────────────────────────
                    Embedding: all-MiniLM-L6-v2 (sentence-transformers)
                    Vector Store: ChromaDB (local)
                    - embed each chunk
                    - store with source filename + chunk index
                                        │
                                        ▼
                    [4] Retrieval                   [5] Generation
                    ──────────────────────          ──────────────────────────
                    Tool: ChromaDB query            Tool: Groq (llama-3.3-70b-versatile)
                    - semantic similarity search    - prompt with retrieved chunks
                    - top-k = 5                     - grounded response only
                    - return chunks + sources       - source attribution in output
                                        │
                                        ▼
                                   [Query Interface]
                                   Tool: Gradio web UI
                                   - text input box
                                   - answer output
                                   - sources output

```

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
I will give Claude this planning.md and ask it to implement two functions: `load_documents(folder_path)` that reads all .txt files and returns a list of `{text, source}` dicts, and `chunk_text(text, chunk_size=400, overlap=80)` that splits text into overlapping character chunks. I will verify the output by printing 5 sample chunks and checking they are complete thoughts, not fragments.

**Milestone 4 — Embedding and retrieval:**
I will give Claude the Retrieval Approach section and the Architecture diagram and ask it to implement `embed_and_store(chunks)` using `sentence-transformers` and `ChromaDB`, and a `retrieve(query, k=5)` function that returns top-k chunks with source metadata. I will verify by running 3 test queries manually and checking that returned chunks are visibly relevant.

**Milestone 5 — Generation and interface:**
I will give Claude the full pipeline context and ask it to implement a `generate_answer(query)` function using the Groq API with a grounding prompt that instructs the model to answer only from retrieved context, and a Gradio UI with a query input box, answer output, and sources output. I will verify grounding by asking a question my documents don't cover and confirming the system refuses rather than hallucinating.
