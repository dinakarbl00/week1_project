# The Unofficial Guide — ASU off campus housing

<!-- > **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit. -->

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This project covers **Tempe off-campus housing for ASU students**, specifically student-generated reviews, Reddit discussions, and tenant experiences about apartment complexes near ASU's Tempe campus.
 
This knowledge is valuable because official ASU housing pages only list affiliated complexes and say nothing about maintenance responsiveness, hidden fees, pest issues, or what it's actually like to live somewhere. A prospective student Googling "apartments near ASU" gets polished marketing pages. The real knowledge: cockroach problems at Agave, sewage smells at Skye, which complexes have predatory move-out charges, which ones are actually walkable to campus, it all lives in Reddit threads and Google Maps reviews that are hard to search systematically. This RAG system makes that scattered, informal knowledge answerable through plain-language questions.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Agave Apartments — Google Maps reviews | Google Maps reviews | https://www.google.com/maps/place/Agave/@33.409112,-111.9241147 |
| 2 | The Piedmont by Mark-Taylor — Google Maps reviews | Google Maps reviews | https://www.google.com/maps/place/The+Piedmont/@33.4242746,-111.9281299 |
| 3 | Skye at McClintock Station — Google Maps reviews | Google Maps reviews | https://www.google.com/maps/place/Skye+at+McClintock+Station/@33.4140004,-111.9065104 |
| 4 | Skywater at Tempe Town Lake — Google Maps reviews | Google Maps reviews | https://www.google.com/maps/place/Skywater+at+Tempe+Town+Lake/@33.4303458,-111.9482323 |
| 5 | IMT Desert Palm Village — ApartmentRatings.com | Verified tenant reviews | https://www.apartmentratings.com/az/tempe/imt-desert-palm-village_480968109985281/ |
| 6 | Allure at Tempe — ApartmentRatings.com | Verified tenant reviews | https://www.apartmentratings.com/az/tempe/allure-at-tempe-apartments_480839946985283/ |
| 7 | r/ASU — "What apartments are good in Tempe near ASU?" | Reddit thread | https://www.reddit.com/r/ASU/comments/1np68lm/what_apartments_are_good_in_tempe_near_asu/ |
| 8 | r/ASU — "Cheap apartments near ASU Tempe recommendations?" | Reddit thread | https://www.reddit.com/r/ASU/comments/1d6osqa/cheap_apartments_near_asu_tempe_recommendations/ |
| 9 | r/ASU — "Off campus freshman year" | Reddit thread | https://www.reddit.com/r/ASU/comments/19dtoqo/off_campus_freshman_year/ |
| 10 | r/ASU — "Is there a reason most students live off campus?" | Reddit thread | https://www.reddit.com/r/ASU/comments/s1jwkv/is_there_a_reason_most_students_live_off_campus/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Why these choices fit your documents:**

My documents has two types of text. Reviews from Google Maps and ApartmentRatings are short and opinionated, usually a few sentences about one thing, like maintenance or noise. Reddit threads run longer, but each reply is really just one person's take.

So I treat every review and every Reddit reply as its own retrievable unit. Chunk too small (say 100 characters) and a single thought gets sliced in half, leaving neither piece useful. Chunk too big (1000 characters) and you end up blending multiple views, often very different, into one embedding, which muddies the signal and tanks retrieval.

400 characters fits one review or reply while staying on a single topic. The 80-character overlap is just insurance.

Before chunking, documents were cleaned to remove: HTML artifacts, advertiser promotions embedded in Reddit pages, management owner responses (which are PR, not tenant opinions), navigation boilerplate, and SOURCE header lines that would otherwise be embedded as if they were content.

**Final chunk count:** 247 chunks across 10 documents

---

## Sample Chunks
 
Below are 5 representative chunks with their source documents.
 
**Chunk 1** — `skye_mclintock_google_reviews.txt`
```
Fourton Miles
5 months ago
I lived at Skye at McClintock Station for nearly a year, and my experience was consistently frustrating due to mismanagement, maintenance issues, and unsanitary conditions.
```
 
**Chunk 2** — `reddit_asu_cheap_apts.txt`
```
Alight will definitely do just fine if you need it to. Probably with roommates though. A group of my friends have a 4 bed 4 bath there right now for $840 utilities included. It probably went up for this coming year but still one of the more reasonable ones. If you can grab a UPass the train from McClintock and Apache to ASU is hella convenient.
```
 
**Chunk 3** — `agave_google_reviews.txt`
```
Ryan
7 months ago
Bad management, old building and cockroaches. These apartments are decent but so poorly managed that they are not worth the price.
```
 
**Chunk 4** — `reddit_asu_why_offcampus.txt`
```
I paid like $4k each semester for one of the worst dorms in the school (PV west), while I was a freshman. During my sophomore year, I was able to rent a nice apartment at Union Tempe for around the same price and not have to share a bathroom with 3 others, or share a kitchen/living room with a whole floor, and had an in-unit washer/dryer.
```
 
**Chunk 5** — `piedmont_google_reviews.txt`
```
Beatrix Cobb
3 months ago
I can't wait to get out of this apartment. They claim to be luxury, but all they care about is appearances in the lobby and common areas. I had severe mold in my shower, and when they finally fixed it, they painted the new wall the wrong color.
```
 
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:**
For this project, `all-MiniLM-L6-v2` is a practical choice — it runs locally with no API key or rate limits, has reasonable accuracy on short opinion text, and produces 384-dimensional embeddings that are fast to query in ChromaDB.

For a production deployment serving real students, I would weigh several tradeoffs:
 
- **Context length:** `all-MiniLM-L6-v2` truncates at 256 tokens. For longer Reddit threads, this means some chunk content gets silently dropped during embedding. A model like `text-embedding-3-small` (OpenAI) or `embed-english-v3.0` (Cohere) supports longer contexts and may produce better embeddings for multi-sentence chunks.
- **Accuracy on domain-specific text:** Student slang and apartment-specific terminology ("in-unit W/D", "UPass", "per-bed lease") may not be well-represented in a general-purpose model. A fine-tuned or larger model would handle this better.
- **Local vs. API-hosted:** Running locally avoids cost and latency from network calls but limits model size. For production with many concurrent users, an API-hosted embedding service with batching would be more scalable.
- **Multilingual support:** ASU has a large international student population. A multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` might surface relevant reviews written in other languages.

Top-k of 5 balances giving the LLM enough context to synthesize an answer while avoiding dilution from loosely related chunks. Too few (k=2) risks missing the most relevant review if retrieval isn't perfect; too many (k=10) risks flooding the prompt with off-topic content.

---

## Retrieval Test Results
 
**Query 1:** "What do students say about maintenance at Skye at McClintock Station?"
 
Top returned chunks:
- `skye_mclintock_google_reviews.txt` (distance: 0.801) — Fourton Miles review mentioning mismanagement and maintenance issues
- `skye_mclintock_google_reviews.txt` (distance: 0.953) — Review praising Baylee during move-in
- `imt_desert_palm_apartmentratings.txt` (distance: 1.102) — Maintenance review from a different complex
*Why the top chunk is relevant:* The first result directly mentions "maintenance issues" and "mismanagement" at Skye at McClintock Station by name, which directly matches the query. The second result is from the right source but discusses move-in support rather than ongoing maintenance — partially relevant.
 
---
 
**Query 2:** "What are the cheapest apartment options near ASU Tempe?"
 
Top returned chunks:
- `reddit_asu_apt_recommendations.txt` (distance: 0.412) — Thread specifically about apartment recommendations near ASU
- `reddit_asu_cheap_apts.txt` (distance: 0.437) — Thread titled "Cheap Apartments near ASU Tempe recommendations"
- `reddit_asu_apt_recommendations.txt` (distance: 0.532) — Discussion of affordable options
*Why the top chunks are relevant:* Both top results come from Reddit threads specifically focused on affordable housing near ASU — the query vocabulary ("cheap", "near ASU Tempe") closely matches thread titles and content. Distance scores under 0.5 indicate strong semantic alignment.
 
---
 
**Query 3:** "Are there any reports of mold or pest problems in Tempe apartments?"
 
Top returned chunks:
- `tempe_complex2_apartmentratings.txt` (distance: 0.863) — Review mentioning roaches at Allure at Tempe
- `reddit_asu_why_offcampus.txt` (distance: 0.879) — Warning about black mold at Murietta at ASU
- `tempe_complex2_apartmentratings.txt` (distance: 0.924) — Review mentioning dog poop and cleanliness issues
*Why the top chunks are relevant:* Result 2 directly surfaces a black mold warning from a Reddit post about a Priderock-managed complex near ASU. Result 1 mentions roaches at Allure at Tempe. Both are genuine pest/mold reports from different sources, showing the system is pulling from multiple document types.
 
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt passed to `llama-3.3-70b-versatile` via Groq contains these explicit rules:
 
```
CRITICAL RULES:
1. Answer ONLY using the information provided in the sources below.
2. Do NOT use any outside knowledge or make assumptions beyond what is in the sources.
3. Always cite which source(s) your answer draws from.
4. If the provided sources do not contain enough information to answer the question,
   respond with exactly: "I don't have enough information in my documents to answer
   that question."
5. Do not make up apartment names, prices, or experiences not mentioned in the sources.
```

**How source attribution is surfaced in the response:**
Each retrieved chunk is labeled with its filename before being passed to the model (e.g. `[Source 1: skye_mclintock_google_reviews.txt]`). The model is instructed to cite these labels in its response. Additionally, the Gradio UI displays a separate "Retrieved from these sources" box that programmatically lists the source filenames of all retrieved chunks, independent of what the model chooses to mention — so attribution is guaranteed at the pipeline level even if the model omits a citation.

---

## Example Responses
 
**Example 1 — Grounded response with source attribution:**
 
Query: *"What do students say about maintenance at Skye at McClintock Station?"*
 
Response:
> According to skye_mclintock_google_reviews.txt, students have mixed experiences with maintenance at Skye at McClintock Station. Fourton Miles mentions "maintenance issues" as one of the reasons for their frustrating experience (Source 1: skye_mclintock_google_reviews.txt). mason dzon implies that the leasing office is unresponsive, which may relate to maintenance requests (Source 5: skye_mclintock_google_reviews.txt).
 
Sources shown: `skye_mclintock_google_reviews.txt`, `imt_desert_palm_apartmentratings.txt`, `skywater_google_reviews.txt`
 
---
 
**Example 2 — Grounded response with multi-source attribution:**
 
Query: *"Are there any reports of mold or pest problems in Tempe apartments?"*
 
Response:
> According to Source 2: reddit_asu_why_offcampus.txt, there is a report of black mold at a complex managed by Priderock Capital Partners, as mentioned in an ABC12 news story. Additionally, Source 5: agave_google_reviews.txt mentions cockroaches at Agave Apartments. Source 1 and Source 3 from tempe_complex2_apartmentratings.txt mention cleanliness issues at Allure at Tempe including dog waste throughout the property.
 
Sources shown: `tempe_complex2_apartmentratings.txt`, `reddit_asu_why_offcampus.txt`, `agave_google_reviews.txt`
 
---
 
**Example 3 — Out-of-scope refusal:**
 
Query: *"What is the best time to visit the moon?"*
 
Response:
> I don't have enough information in my documents to answer that question.
 
---

## Query Interface
 
The interface is a Gradio web app (`app.py`) running at `http://localhost:7860`.
 
**Input field:** A text box labeled "Your Question" where the user types a plain-language question about Tempe off-campus housing.
 
**Output fields:**
- "Answer" — a multi-line text box showing the LLM's grounded response with inline source citations
- "Retrieved from these sources" — a separate text box listing the filenames of all chunks retrieved for that query
The user can submit by clicking the "Ask" button or pressing Enter. Example questions are shown at the bottom of the interface.
 
**Sample interaction transcript:**
 
```
User input:  Do students recommend living off campus instead of ASU dorms? Why?
 
Answer:      According to the sources, some students recommend living off campus
             instead of ASU dorms, while others suggest dorm life is valuable for
             socialization. One student notes that off campus provides more privacy
             and saves money, with commuting as the only downside
             (Source 3: reddit_asu_offcampus_freshman.txt). Another mentions paying
             $4k per semester for a bad dorm (PV West) as a freshman, then renting
             a nicer apartment for the same price with in-unit washer/dryer
             (Source 5: reddit_asu_why_offcampus.txt). ASU also converts most
             upper-division dorms to freshman housing, leaving upperclassmen with
             very few on-campus options (Source 5: reddit_asu_why_offcampus.txt).
 
Retrieved from: • reddit_asu_offcampus_freshman.txt
                • reddit_asu_why_offcampus.txt
                • reddit_asu_cheap_apts.txt
```
 
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about maintenance at Skye at McClintock Station? | Mixed reviews — complaints about mismanagement, slow maintenance, dirty hallways; some positive staff experiences | Found maintenance complaints and unresponsive office mentions from Skye reviews, but missed specific issues like flooding and sewage | Partially relevant | Partially accurate |
| 2 | Is Agave Apartments walkable to ASU campus? | Yes — at least one review mentions walking distance to ASU | Returned "I don't have enough information" despite walkability being mentioned in documents | Off-target | Inaccurate |
| 3 | What are the cheapest apartment options near ASU Tempe? | Alight (~$840 with roommates), Yugo, Metro 101/Access mentioned by students | Found the right Reddit threads but failed to surface specific apartment names and prices from within those threads | Partially relevant | Partially accurate |
| 4 | Do students recommend living off campus instead of ASU dorms? Why? | Yes — cheaper, more freedom, in-unit amenities, limited upper-division dorm availability | Accurately synthesized multiple perspectives including cost comparison, privacy, commute tradeoff, and ASU dorm scarcity | Relevant | Accurate |
| 5 | Are there any reports of mold or pest problems in Tempe apartments? | Cockroaches at Agave, mold at The Piedmont, black mold warning for Murietta at ASU | Found black mold warning from Reddit and cockroaches at Agave; missed mold at The Piedmont | Relevant | Accurate |

<!-- **Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate -->

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Is Agave Apartments walkable to ASU campus?"

**What the system returned:** "I don't have enough information in my documents to answer that question."

**Root cause (tied to a specific pipeline stage):**
This is a retrieval failure caused by vocabulary mismatch at the embedding stage. The query uses the word "walkable" but the relevant review in `agave_google_reviews.txt` uses the phrase "walking distance to ASU." These phrases are semantically similar to a human reader but `all-MiniLM-L6-v2` did not produce embeddings close enough for the chunk to surface in the top-5 results.

**What you would change to fix it:**
Two options: (1) increase top-k from 5 to 8–10 to cast a wider retrieval net, accepting some dilution in exchange for higher recall; or (2) implement query expansion — before embedding the query, rephrase it to include synonyms like "walking distance", "close to campus", "near ASU" — so the embedding is more likely to match the phrasing used in reviews.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing the chunking strategy in `planning.md` before writing any code forced a concrete decision about chunk size before seeing the actual output. When the first version of `embed.py` returned distance scores above 0.95 for the Skye maintenance query, I had a documented rationale to check against, the spec said chunks should hold "one complete review or one Reddit reply." That made it clear the problem was the SOURCE URL headers being embedded as chunks, not the chunk size itself. Without the spec, I would have changed chunk size first and wasted time debugging the wrong thing.

**One way your implementation diverged from the spec, and why:**
The spec anticipated 5 stretch features as optional additions after the core pipeline. In practice, the cleaning pipeline needed two full revision passes — one to remove ads and one to remove owner responses — that were not planned for in `planning.md`. These were discovered only by inspecting actual chunk output, which the spec's "print 5 random chunks" checkpoint made mandatory. The time spent on these cleaning passes came at the cost of not implementing any stretch features before the submission deadline.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**: Ingestion and chunking pipeline

- *What I gave the AI:* The Documents section and Chunking Strategy section from `planning.md`, specifying 400-character chunks with 80-character overlap and the need to attach source metadata to each chunk.
- *What it produced:* `ingest.py` with `load_documents()` and `chunk_text()` functions using character-based splitting with overlap. The initial version included the SOURCE header line in the text before chunking.
- *What I changed or overrode:* After running the script and seeing distance scores above 0.95 in retrieval tests, I identified that URL header chunks were being embedded as content. I directed the AI to add a filtering step in `load_documents()` to strip lines starting with "SOURCE:" before chunking. I also added the `len(chunk) > 50` guard to skip trivially short leftover chunks, which the generated code did not include.

**Instance 2**: Cleaning pipeline for ads and owner responses

- *What I gave the AI:* Sample raw document text showing the two noise types: Reddit ad blocks and apartment management responses.
- *What it produced:* An expanded skip-patterns list and a block-detection approach for multi-line owner responses using an `in_owner_block` flag.
- *What I changed or overrode:* he generated code used `skip_patterns` (raw strings) in one place and `skip_compiled` (compiled regexes) in another, causing an `AttributeError`. I identified the bug, fixed the reference inconsistency, and verified the fix by re-running the cleaning script and inspecting 5 sample chunks manually to confirm owner responses were gone.
