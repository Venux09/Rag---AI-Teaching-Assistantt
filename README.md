# Syllo — AI Teaching Assistant (v1.0)

Syllo is a retrieval-augmented AI assistant that turns a library of course videos into a searchable, question-answering tutor. Point it at a set of lecture videos, and it transcribes them, indexes every moment as a searchable vector, and answers student questions by pulling the exact clip and timestamp where the topic is actually taught — instead of making the student re-watch the whole course.

This is version **1.0**: the core pipeline (transcription → chunking → embeddings → retrieval → generation) works end to end. There's no frontend yet — it currently runs as a CLI, by design, while the retrieval and answer quality get worked on first.

---

## What it does

- Ingests raw course videos and converts them to timestamped, searchable text
- Embeds every chunk of teaching into a vector space
- Answers a student's question using only what's actually taught in the indexed videos (no hallucinated content)
- Always tells the student *which video* and *what timestamp* to go watch

---

## How it works

The project is a straight-line pipeline. Each stage is its own script, and each stage's output feeds the next:

| Step | File | What it does |
|---|---|---|
| 1 | `video_to_audio.py` | Extracts audio from each course video (ffmpeg), named by tutorial number |
| 2 | `create_json.py` | Runs Whisper (small) in translate mode, producing timestamped segments in English regardless of source language |
| 3 | `jsons_cleaning.py` | Strips empty or malformed transcript segments |
| 4 | `merge_json.py` | Groups every 5 segments into one chunk, so retrieval works on coherent stretches of teaching rather than single fragments |
| 5 | `pre_processed.py` | Embeds every chunk (bge-m3) and stores vectors + text + timestamps in `embeddings.joblib` |
| 6 | `process_incoming.py` | CLI entry point: embeds a question, ranks chunks by cosine similarity, asks a local LLM (Ollama) to answer using only the retrieved context |

**Retrieval is meaning-based, not keyword-based** — a question doesn't need to match the exact words used in the lecture, just the underlying concept, since everything is compared by embedding similarity.

**The assistant is grounded** — the prompt sent to the LLM explicitly restricts it to answering only from the retrieved chunks, and to say so plainly when a question falls outside what's indexed.

---

## Tech stack

- **Transcription:** Whisper (small)
- **Embeddings:** bge-m3 (served locally, e.g. via LM Studio)
- **Generation:** Llama 3.2 (1B) via Ollama, local inference
- **Retrieval:** scikit-learn cosine similarity over `embeddings.joblib`

---

## Getting started

1. Put your source videos in a `videos/` folder.
2. Run the pipeline in order:
   ```
   python video_to_audio.py
   python create_json.py
   python jsons_cleaning.py
   python merge_json.py
   python pre_processed.py
   ```
3. Make sure LM Studio (embeddings, port 1234) and Ollama (generation, port 11434) are running locally.
4. Ask a question:
   ```
   python process_incoming.py
   ```

---

## Roadmap — where this is going

v1.0 proves the pipeline works. The plan from here:

- **Accuracy improvements**
  - Better chunking strategy (semantic/overlapping chunks instead of fixed groups of 5)
  - Re-ranking retrieved chunks before generation, not just raw cosine similarity
  - Evaluation set to actually measure answer quality instead of eyeballing it

- **Move beyond a fixed local ML stack**
  - Introduce a proper ML framework layer (e.g. PyTorch/HuggingFace) instead of calling external local servers for embeddings and generation
  - Make the embedding model and LLM swappable without touching the retrieval code

- **Train / fine-tune on different data**
  - Generalize the pipeline so it isn't tied to one course's structure or language
  - Fine-tune a smaller model specifically on teaching-assistant-style answers (grounded, cites timestamps, admits when something isn't covered)
  - Support multiple courses/datasets indexed side by side

- **New features**
  - Multi-turn conversation memory (currently every question is independent)
  - Admin tooling for re-indexing or adding new videos without re-running scripts manually
  - Basic usage analytics (which topics get asked about most, which videos are under-indexed)
  - A frontend, once the underlying answer quality and retrieval are solid enough to be worth building a UI around

- **Productionization**
  - Move off local-only inference (Ollama/LM Studio) toward a deployable inference setup
  - Add auth if this ever needs to support more than one user
  - Persist question/answer history

---

## Status

Actively evolving. Frontend is intentionally deferred — the priority right now is getting the retrieval and answer quality right before building a UI on top of it. This README will be updated as the ML framework, fine-tuning, and multi-dataset support land.


## syllo-journey:
File named as syllo is an interactive expalnation of this project and future plans and why i buided This
Open file in the integeratted grammer 
