# RAG Document Chatbot

A Python Retrieval-Augmented Generation application that allows users to ask questions about local PDF documents.

This project was built incrementally using Python, LangChain, Chroma DB, and OpenAI embeddings.

## Project Goal

The goal of this project is to build a local document chatbot that can:

- Load PDF documents from a local folder
- Split documents into smaller text chunks
- Convert chunks into embeddings
- Store embeddings in a local Chroma vector database
- Retrieve relevant chunks based on a user question
- Generate an answer using an LLM with retrieved context

## Tech Stack

- Python
- LangChain
- Chroma DB
- OpenAI API
- PyPDF
- python-dotenv
- Git/GitHub

## Project Structure

```text
rag-doc-chatbot/
│
├── data/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── check_env.py
│   ├── load_documents.py
│   ├── split_documents.py
│   ├── get_embedding_function.py
│   ├── create_database.py
│   └── query_data.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt