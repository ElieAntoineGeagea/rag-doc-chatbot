from question_router import route_question
from query_rewriter import rewrite_query_for_retrieval


def plan_retrieval_queries(question):
    route = route_question(question)
    rewritten_query = rewrite_query_for_retrieval(question)

    queries = [rewritten_query]

    if route == "summary":
        queries.append("document summary overview main points key information")
        queries.append("important details skills education projects experience")

    elif route == "source_question":
        queries.append("source page document evidence location")
        queries.append("relevant information page number document section")

    elif route == "comparison":
        queries.append("education academic background university degree")
        queries.append("projects machine learning AI RAG chatbot Streamlit")
        queries.append("skills technical experience Python LangChain Chroma")

    elif route == "general_rag":
        queries.append(question)

    clean_queries = []

    for query in queries:
        if query and query not in clean_queries:
            clean_queries.append(query)

    return clean_queries


if __name__ == "__main__":
    test_questions = [
        "Summarize this document",
        "Which page contains the skills?",
        "Compare the education and projects",
        "What are the main skills mentioned?",
        "",
    ]

    for question in test_questions:
        queries = plan_retrieval_queries(question)

        print(f"Question: {question}")
        print("Planned retrieval queries:")

        for index, query in enumerate(queries, start=1):
            print(f"{index}. {query}")

        print("---")