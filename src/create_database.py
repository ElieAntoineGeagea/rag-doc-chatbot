import os
import shutil

from langchain_chroma import Chroma

from load_documents import load_documents
from split_documents import split_documents
from get_embedding_function import get_embedding_function


CHROMA_PATH = "chroma"


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def save_to_chroma(chunks):
    clear_database()

    embedding_function = get_embedding_function()

    vector_store = Chroma(
        collection_name="rag_documents",
        embedding_function=embedding_function,
        persist_directory=CHROMA_PATH,
    )

    vector_store.add_documents(documents=chunks)

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    save_to_chroma(chunks)