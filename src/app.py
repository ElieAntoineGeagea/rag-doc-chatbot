import streamlit as st

from query_data import query_rag


st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
    layout="wide",
)


st.title("📄 RAG Document Chatbot")

st.write(
    "Ask questions about your local PDF documents using Retrieval-Augmented Generation."
)


with st.sidebar:
    st.header("Project Info")

    st.write(
        "This app loads PDF documents, stores them in Chroma DB, "
        "retrieves relevant chunks, and generates answers using an LLM."
    )

    st.subheader("Pipeline")

    st.markdown(
        """
        1. Load PDF documents  
        2. Split text into chunks  
        3. Create embeddings  
        4. Store vectors in Chroma DB  
        5. Retrieve relevant chunks  
        6. Generate an answer  
        """
    )

    st.subheader("Security")

    st.write(
        "API keys, local documents, virtual environment files, "
        "and Chroma database files are ignored by Git."
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("Clear chat"):
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Sources"):
                for index, source in enumerate(message["sources"], start=1):
                    st.markdown(f"**Source {index}**")
                    st.write(f"File: `{source['source']}`")
                    st.write(f"Page: `{source['page']}`")
                    st.write(f"Chunk ID: `{source['id']}`")
                    st.write(f"Similarity score: `{source['score']}`")


question = st.chat_input("Ask a question about your documents")


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            result = query_rag(question)

        st.write(result["answer"])

        if result["sources"]:
            with st.expander("Sources"):
                for index, source in enumerate(result["sources"], start=1):
                    st.markdown(f"**Source {index}**")
                    st.write(f"File: `{source['source']}`")
                    st.write(f"Page: `{source['page']}`")
                    st.write(f"Chunk ID: `{source['id']}`")
                    st.write(f"Similarity score: `{source['score']}`")
        else:
            st.write("No sources found.")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        }
    )