import streamlit as st

from query_data import query_rag


st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
)


st.title("RAG Document Chatbot")

st.write(
    "Ask a question about the PDF documents stored in your local data folder."
)


question = st.text_input("Your question:")


if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):
            result = query_rag(question)

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")

        if result["sources"]:
            for source in result["sources"]:
                st.write(
                    f"Source: {source['source']} | "
                    f"Page: {source['page']} | "
                    f"ID: {source['id']} | "
                    f"Score: {source['score']}"
                )
        else:
            st.write("No sources found.")