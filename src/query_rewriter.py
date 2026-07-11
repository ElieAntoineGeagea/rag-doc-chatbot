from question_router import route_question


def rewrite_query_for_retrieval(question):
    route = route_question(question)

    if route == "summary":
        return f"{question} summary main points overview key information"

    if route == "source_question":
        return f"{question} source page document location evidence"

    if route == "comparison":
        return f"{question} compare differences similarities skills education projects experience"

    if route == "general_rag":
        return question

    return ""
    

if __name__ == "__main__":
    test_questions = [
        "Summarize this document",
        "Which page contains the skills?",
        "Compare the education and projects",
        "Is he good for AI engineering?",
        "",
    ]

    for question in test_questions:
        rewritten_query = rewrite_query_for_retrieval(question)

        print(f"Original question: {question}")
        print(f"Rewritten query: {rewritten_query}")
        print("---")