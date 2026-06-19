from langchain_community.document_loaders import PyPDFDirectoryLoader

DATA_PATH = "data"


def load_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} document pages.")

    if documents:
        print("First page preview:")
        print(documents[0].page_content[:500])