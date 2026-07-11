def route_question(question):
    question_lower= question.lower()

    if any(word in question_lower for word in ["summarize", "summary", " main points"]):
        return "summary"

    if any(word in question_lower for word in ["source", "page", "website", "where", "wich document"]):
        return "source_question"

    if any(word in question_lower for word in ["compare", "difference", "better", "more suitable"]):
        return  "comparison"
    
    if question_lower.strip():
        return "general_rag"
    
    return "unknown"


if __name__ == "__main__":
    test_questions = [
        "Summarize this document",
        "Which page contains the skills?",
        "Compare the education and projects",
        "What are the main skills mentioned?",
        "",
    ]

    for question in test_questions:
        route = route_question(question)
        print(f"Question: {question}")
        print(f"Route: {route}")
        print("---")