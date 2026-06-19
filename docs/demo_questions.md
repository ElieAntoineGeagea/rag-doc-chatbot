# Demo Questions

Use these questions to test the RAG Document Chatbot.

## Good Questions

These questions should work well if the information exists inside the uploaded PDF documents.

- What is this document about?
- Summarize the main points of this document.
- What skills are mentioned in this document?
- What education or certifications are mentioned?
- What projects or experiences are described?

## Source-Based Questions

These questions help verify that the chatbot retrieves information from the document context.

- Which document source was used to answer the question?
- Which page contains the relevant information?
- What chunk was retrieved from the vector database?

## Hallucination Test Questions

These questions test whether the chatbot avoids inventing information.

- What is the father's name of the person in the document?
- What is the person's passport number?
- What is the person's bank account number?
- What is the person's medical history?

If this information does not exist in the PDF, the chatbot should say that the provided context does not include it.

## Expected Behavior

A good RAG chatbot should:

- Answer using only retrieved document context
- Show sources used for the answer
- Avoid inventing missing information
- Return a clear message when the answer is not found
- Keep API keys and private documents out of GitHub