from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


def get_embedding_function():
    load_dotenv()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return embeddings


if __name__ == "__main__":
    embedding_function = get_embedding_function()

    result = embedding_function.embed_query("This is a test sentence.")

    print(f"Embedding created successfully.")
    print(f"Vector length: {len(result)}")
    print(f"First 5 values: {result[:5]}")