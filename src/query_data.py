import argparse
import os

from dotenv import load_dotenv
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
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "answer": "OPENAI_API_KEY was not found. Please check your local .env file.",
            "sources": [],
        }

    if not os.path.exists(CHROMA_PATH):
        return {
            "answer": "Chroma database not found. Run python src/create_database.py --reset first.",
            "sources": [],
        }

    try:
        embedding_function = get_embedding_function()

        db = Chroma(
            collection_name="rag_documents",
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function,
        )

        results = db.similarity_search_with_score(query_text, k=3)

        if not results:
            return {
                "answer": "No relevant results found.",
                "sources": [],
            }

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

        sources = []

        for doc, score in results:
            source_info = {
                "source": doc.metadata.get("source", "Unknown source"),
                "page": doc.metadata.get("page", "Unknown page"),
                "id": doc.metadata.get("id", "No ID"),
                "score": round(score, 4),
            }

            sources.append(source_info)

        return {
            "answer": response.content,
            "sources": sources,
        }

    except Exception as error:
        return {
            "answer": f"An error occurred while querying the RAG system: {error}",
            "sources": [],
        }


def print_result(result):
    print("Answer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"Source: {source['source']} | "
            f"Page: {source['page']} | "
            f"ID: {source['id']} | "
            f"Score: {source['score']}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "query_text",
        type=str,
        help="The question to ask your documents.",
    )

    args = parser.parse_args()

    result = query_rag(args.query_text)

    print_result(result)