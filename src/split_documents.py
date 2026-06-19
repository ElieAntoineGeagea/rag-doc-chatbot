from load_documents import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 800
CHUNK_OVERLAP = 80


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} document pages.")
    print(f"Split into {len(chunks)} chunks.")

    if chunks:
        print("First chunk preview:")
        print(chunks[0].page_content[:500])

        print("First chunk metadata:")
        print(chunks[0].metadata)