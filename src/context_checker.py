MIN_CONTEXT_CHARACTERS = 100


def check_context_sufficiency(results, route):
    if not results:
        return {
            "is_sufficient": False,
            "reason": "No retrieved document chunks were found.",
        }

    context_length = 0

    for doc, _score in results:
        context_length += len(doc.page_content.strip())

    if context_length < MIN_CONTEXT_CHARACTERS:
        return {
            "is_sufficient": False,
            "reason": "The retrieved context is too short to answer reliably.",
        }

    if route == "comparison" and len(results) < 2:
        return {
            "is_sufficient": False,
            "reason": "Comparison questions need at least two relevant chunks.",
        }

    return {
        "is_sufficient": True,
        "reason": "The retrieved context is sufficient.",
    }


if __name__ == "__main__":
    from langchain_core.documents import Document

    fake_results = [
        (
            Document(
                page_content="This document mentions education, projects, machine learning, Python, and AI engineering experience.",
                metadata={"source": "fake.pdf", "page": 0},
            ),
            0.5,
        ),
        (
            Document(
                page_content="The project section describes a RAG chatbot, machine learning projects, and technical skills.",
                metadata={"source": "fake.pdf", "page": 1},
            ),
            0.7,
        ),
    ]

    result = check_context_sufficiency(fake_results, "comparison")

    print(result)