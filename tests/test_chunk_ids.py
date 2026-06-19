from langchain_core.documents import Document

from create_database import calculate_chunk_ids


def test_calculate_chunk_ids():
    chunks = [
        Document(
            page_content="First chunk",
            metadata={"source": "data/test.pdf", "page": 0},
        ),
        Document(
            page_content="Second chunk",
            metadata={"source": "data/test.pdf", "page": 0},
        ),
        Document(
            page_content="Third chunk",
            metadata={"source": "data/test.pdf", "page": 1},
        ),
    ]

    chunks_with_ids = calculate_chunk_ids(chunks)

    assert chunks_with_ids[0].metadata["id"] == "data/test.pdf:0:0"
    assert chunks_with_ids[1].metadata["id"] == "data/test.pdf:0:1"
    assert chunks_with_ids[2].metadata["id"] == "data/test.pdf:1:0"