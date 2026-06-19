import argparse
import os
import shutil

from langchain_chroma import Chroma

from load_documents import load_documents
from split_documents import split_documents
from get_embedding_function import get_embedding_function


CHROMA_PATH = "chroma"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset the Chroma database before adding documents.",
    )

    args = parser.parse_args()

    if args.reset:
        print("Clearing database...")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    chunks_with_ids = calculate_chunk_ids(chunks)
    add_to_chroma(chunks_with_ids)


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")

        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id

        last_page_id = current_page_id

    return chunks


def add_to_chroma(chunks):
    db = Chroma(
        collection_name="rag_documents",
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function(),
    )

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    print(f"Existing documents in DB: {len(existing_ids)}")

    new_chunks = []

    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]

        db.add_documents(
            documents=new_chunks,
            ids=new_chunk_ids,
        )

        print(f"Added {len(new_chunks)} new chunks to Chroma.")
    else:
        print("No new chunks to add.")


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()