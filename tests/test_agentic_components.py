from langchain_core.documents import Document

from question_router import route_question
from query_rewriter import rewrite_query_for_retrieval
from retrieval_planner import plan_retrieval_queries
from context_checker import check_context_sufficiency


def test_route_question_comparison():
    route = route_question("Compare the education and projects")

    assert route == "comparison"


def test_rewrite_query_for_comparison():
    rewritten_query = rewrite_query_for_retrieval(
        "Compare the education and projects"
    )

    assert "education" in rewritten_query
    assert "projects" in rewritten_query
    assert "experience" in rewritten_query


def test_plan_retrieval_queries_for_comparison():
    queries = plan_retrieval_queries("Compare the education and projects")

    assert len(queries) >= 4
    assert any("education" in query for query in queries)
    assert any("projects" in query for query in queries)
    assert any("skills" in query for query in queries)


def test_context_checker_with_sufficient_context():
    fake_results = [
        (
            Document(
                page_content=(
                    "This document contains education information, university "
                    "background, AI projects, machine learning experience, "
                    "Python skills, and technical project details."
                ),
                metadata={"source": "fake.pdf", "page": 0},
            ),
            0.5,
        ),
        (
            Document(
                page_content=(
                    "The project section describes a RAG chatbot, Streamlit app, "
                    "LangChain, Chroma DB, embeddings, and AI engineering skills."
                ),
                metadata={"source": "fake.pdf", "page": 1},
            ),
            0.7,
        ),
    ]

    context_check = check_context_sufficiency(fake_results, "comparison")

    assert context_check["is_sufficient"] is True
    assert context_check["reason"] == "The retrieved context is sufficient."


def test_context_checker_with_no_results():
    context_check = check_context_sufficiency([], "general_rag")

    assert context_check["is_sufficient"] is False
    assert context_check["reason"] == "No retrieved document chunks were found."