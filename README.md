# RAG Document Chatbot with Agentic RAG

## Overview

This project is an AI-powered document chatbot built with Python, LangChain, Chroma DB, OpenAI API, and Streamlit.

The chatbot allows users to ask questions about local PDF documents. It loads PDF files, splits them into chunks, converts the chunks into embeddings, stores them in a local Chroma vector database, retrieves relevant chunks, and generates answers using an LLM.

The project was later upgraded from a standard RAG chatbot into an agentic RAG chatbot by adding question routing, query rewriting, retrieval planning, multi-query retrieval, context sufficiency checking, and an agentic trace inside the Streamlit interface.

---

## Project Goal

The goal of this project is to build a complete Retrieval-Augmented Generation chatbot that can:

* Answer questions from local PDF documents.
* Retrieve relevant document chunks using semantic search.
* Generate answers using an LLM.
* Show the sources used to produce the answer.
* Avoid answering when the retrieved context is not sufficient.
* Display the agentic reasoning trace used before answering.

---

## Tech Stack

* Python
* LangChain
* Chroma DB
* OpenAI API
* Streamlit
* pytest
* Git/GitHub
* python-dotenv
* pypdf

---

## Project Structure

```text
rag-doc-chatbot/
│
├── data/
│   └── .gitkeep
│
├── docs/
│   └── demo_questions.md
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── check_env.py
│   ├── load_documents.py
│   ├── split_documents.py
│   ├── get_embedding_function.py
│   ├── create_database.py
│   ├── query_data.py
│   ├── question_router.py
│   ├── query_rewriter.py
│   ├── context_checker.py
│   └── retrieval_planner.py
│
├── tests/
│   ├── test_chunk_ids.py
│   └── test_agentic_components.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Standard RAG Pipeline

The first version of the project followed a standard RAG pipeline:

```text
User question
→ embed the question
→ search Chroma DB
→ retrieve relevant chunks
→ send context to the LLM
→ generate answer
→ show sources
```

This allowed the chatbot to answer questions based on the content of local PDF documents.

---

## Agentic RAG Upgrade

This project was upgraded from a standard RAG chatbot into an agentic RAG chatbot.

A standard RAG chatbot usually follows a fixed pipeline:

```text
User question → retrieve relevant chunks → generate answer
```

This project now adds an agentic decision layer before answering.

The upgraded pipeline is:

```text
User question
→ classify the question type
→ rewrite the query for better retrieval
→ plan multiple retrieval queries
→ search Chroma DB multiple times
→ remove duplicate chunks
→ check if the retrieved context is sufficient
→ generate a source-grounded answer
```

---

## Agentic Features

The agentic upgrade includes:

* Question routing to classify questions as summary, source-based, comparison, or general RAG questions.
* Route-specific prompt templates for better answer formatting.
* Query rewriting to improve retrieval quality.
* Retrieval planning to create multiple search queries depending on the question type.
* Multi-query Chroma retrieval instead of only one similarity search.
* Duplicate chunk removal after multi-query retrieval.
* Context sufficiency checking before sending the prompt to the LLM.
* Agentic trace display in Streamlit, showing:

  * detected route
  * rewritten query
  * planned retrieval queries
  * context sufficiency result
* Automated tests for agentic components.

---

## Example Agentic Trace

For the question:

```text
Compare the education and projects
```

The chatbot may create this retrieval plan:

```text
Route: comparison

Rewritten query:
Compare the education and projects compare differences similarities skills education projects experience

Planned retrieval queries:
1. Compare the education and projects compare differences similarities skills education projects experience
2. education academic background university degree
3. projects machine learning AI RAG chatbot Streamlit
4. skills technical experience Python LangChain Chroma

Context sufficient: True
Context reason: The retrieved context is sufficient.
```

This makes the chatbot more advanced than a basic PDF chatbot because it can decide how to search, what evidence to collect, and whether the retrieved context is strong enough before answering.

---

## Main Features

* Load local PDF documents.
* Split documents into smaller chunks.
* Generate OpenAI embeddings.
* Store document chunks in Chroma DB.
* Retrieve relevant chunks using semantic search.
* Generate answers using an OpenAI chat model.
* Display document sources.
* Show page numbers and chunk IDs.
* Support Streamlit chat interface.
* Store chat history during the session.
* Clear chat history.
* Handle missing API key errors.
* Handle missing Chroma database errors.
* Handle insufficient context.
* Use query rewriting for better retrieval.
* Use multi-query retrieval planning.
* Display an agentic RAG trace.
* Include automated tests.

---

## Important Files

### `src/load_documents.py`

Loads PDF documents from the local `data/` folder.

### `src/split_documents.py`

Splits documents into smaller chunks using `RecursiveCharacterTextSplitter`.

### `src/get_embedding_function.py`

Creates the OpenAI embedding function using `text-embedding-3-small`.

### `src/create_database.py`

Creates or updates the Chroma vector database.

It supports:

```bash
python src/create_database.py --reset
```

This clears the old Chroma database and rebuilds it.

### `src/query_data.py`

Main RAG query logic.

It:

* routes the question
* rewrites the query
* plans multiple retrieval queries
* searches Chroma DB
* removes duplicate chunks
* checks context sufficiency
* builds the prompt
* calls the LLM
* returns answer, sources, and agentic trace

### `src/question_router.py`

Classifies the question type.

Possible routes:

```text
summary
source_question
comparison
general_rag
unknown
```

### `src/query_rewriter.py`

Rewrites the user question into a better retrieval query.

Example:

```text
Original question:
Compare the education and projects

Rewritten query:
Compare the education and projects compare differences similarities skills education projects experience
```

### `src/retrieval_planner.py`

Plans multiple retrieval queries depending on the route.

For comparison questions, it creates separate searches for:

* education
* projects
* skills
* experience

### `src/context_checker.py`

Checks if the retrieved chunks are sufficient before answering.

### `src/app.py`

Streamlit user interface.

It displays:

* chatbot answer
* sources
* agentic RAG trace
* chat history
* sidebar project information

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd rag-doc-chatbot
```

---

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 4. Create a `.env` File

Create a file named:

```text
.env
```

Inside it, add:

```env
OPENAI_API_KEY=your_real_api_key_here
```

Do not upload this file to GitHub.

---

### 5. Add PDF Documents

Place your PDF files inside:

```text
data/
```

Example:

```text
data/my_document.pdf
```

The `data/` folder is ignored by Git to protect private documents.

---

### 6. Create the Chroma Database

Run:

```bash
python src/create_database.py --reset
```

This will:

* load PDFs
* split documents into chunks
* create embeddings
* save vectors into Chroma DB

---

### 7. Ask Questions from the Terminal

Example:

```bash
python src/query_data.py "Summarize this document"
```

Another example:

```bash
python src/query_data.py "Compare the education and projects"
```

The output includes:

* answer
* route
* rewritten query
* planned retrieval queries
* context sufficiency result
* sources

---

### 8. Run the Streamlit App

```bash
streamlit run src/app.py
```

Then open the local Streamlit link in your browser.

---

## Example Questions

Good questions to test the chatbot:

```text
Summarize this document.
What is this document about?
What skills are mentioned?
Which page contains the skills?
Compare the education and projects.
What are the main projects mentioned?
What experience is described in the document?
```

Hallucination test question:

```text
What is the father’s name of the person in the document?
```

Expected behavior:

The chatbot should not invent an answer. If the information is not in the retrieved context, it should say that the context is insufficient or that the information is not provided.

---

## Testing

This project uses pytest.

Run all tests:

```bash
pytest
```

The tests check:

* chunk ID generation
* question routing
* query rewriting
* retrieval planning
* context sufficiency checking

Expected result:

```text
All tests passed
```

A LangChain warning may appear. This does not necessarily mean the tests failed.

---

## Security Notes

This project is designed to avoid exposing private files and secrets.

The `.gitignore` file excludes:

```gitignore
.venv/
.env
chroma/
data/*
!data/.gitkeep
__pycache__/
*.pyc
```

Meaning:

* `.env` is ignored because it contains the real API key.
* `data/*` is ignored because PDFs may be private.
* `chroma/` is ignored because it contains the local vector database.
* `.venv/` is ignored because virtual environments should not be uploaded.

The repository includes:

```text
.env.example
```

with:

```env
OPENAI_API_KEY=your_api_key_here
```

This is safe because it is only a placeholder.

---

## GitHub Safety Check

Before making the repository public, run:

```bash
git status
git ls-files
git grep "sk-"
git grep "OPENAI_API_KEY="
```

Safe result:

* `.env` should not appear in tracked files.
* real API key should not appear.
* private PDFs should not appear.
* `chroma/` should not appear.
* `.env.example` may appear with a placeholder key.

This is safe:

```text
.env.example:OPENAI_API_KEY=your_api_key_here
```

This is not safe:

```text
OPENAI_API_KEY=sk-...
```

---

## Project Status

Completed version:

* Standard RAG chatbot completed.
* Agentic RAG upgrade completed.
* Streamlit interface completed.
* Source display completed.
* Agentic trace display completed.
* Automated tests completed.
* Security checks completed.
* Git version tag created.
* GitHub repository ready.

Current app status:

```text
Working locally with Streamlit
```

---

## Current Limitations

* The app currently runs locally.
* The project is not deployed publicly.
* The chatbot answers only from local PDF documents.
* Retrieval quality depends on document quality and chunking.
* API usage requires an active OpenAI API key with available credits.

---

## Future Improvements

Possible future upgrades:

* Add support for uploaded PDFs directly in Streamlit.
* Add support for Word documents.
* Add support for multiple document collections.
* Add conversation memory.
* Add web search as an optional tool.
* Add more advanced agent tools.
* Add reranking for better retrieval quality.
* Add evaluation metrics for RAG answers.
* Add deployment on Streamlit Cloud.
* Add Docker support.
* Add authentication for private use.

---


## Strong Project Explanation

I built a complete Retrieval-Augmented Generation chatbot using Python, LangChain, Chroma DB, OpenAI API, and Streamlit. The system loads local PDF documents, splits them into chunks, converts them into embeddings, stores them in a local vector database, retrieves relevant context based on user questions, and generates answers with source tracking. I also upgraded the project into an agentic RAG system by adding question routing, query rewriting, multi-query retrieval planning, context sufficiency checking, and an agentic trace in the Streamlit interface.

---

## Version

```text
v1.0 - First complete RAG document chatbot version
```

Agentic RAG upgrade completed after v1.0.
