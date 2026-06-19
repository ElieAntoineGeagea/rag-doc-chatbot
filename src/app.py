import streamlit as st

from query_data import query_rag


st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
)


st.title("RAG Document Chatbot")

st.write(
    "Ask questions about the PDF documents stored in your local data folder."
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
                for source in message["sources"]:
                    st.write(
                        f"Source: {source['source']} | "
                        f"Page: {source['page']} | "
                        f"ID: {source['id']} | "
                        f"Score: {source['score']}"
                    )


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
                for source in result["sources"]:
                    st.write(
                        f"Source: {source['source']} | "
                        f"Page: {source['page']} | "
                        f"ID: {source['id']} | "
                        f"Score: {source['score']}"
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        }
    )