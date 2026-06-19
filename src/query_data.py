import argparse
import os

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from get_embedding_function import get_embedding_function


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Question: {question}

Answer:
"""


def query_rag(query_text):
    if not os.path.exists(CHROMA_PATH):
        print("Chroma database not found. Please run create_database.py first.")
        return

    embedding_function = get_embedding_function()

    db = Chroma(
        collection_name="rag_documents",
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    results = db.similarity_search_with_score(query_text, k=3)

    if not results:
        print("No relevant results found.")
        return

    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results]
    )

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(
        context=context_text,
        question=query_text,
    )

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    response = model.invoke(prompt)

    print("Answer:")
    print(response.content)

    print("\nSources:")
    for doc, score in results:
        print(f"Source: {doc.metadata} | Score: {score}")

    return response.content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "query_text",
        type=str,
        help="The question to ask your documents.",
    )

    args = parser.parse_args()

    query_rag(args.query_text)