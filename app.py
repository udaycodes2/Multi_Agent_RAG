# import os
# import streamlit as st

# from graph import graph
# from rag import (
#     create_vectorstore,
#     save_vectorstore
# )

# st.set_page_config(
#     page_title="AI Research Assistant",
#     layout="wide"
# )

# st.title("AI Research Assistant")

# uploaded_files = st.sidebar.file_uploader(
#     "Upload PDF Files",
#     type=["pdf"],
#     accept_multiple_files=True
# )

# use_pdf = st.sidebar.checkbox(
#     "Use uploaded PDFs",
#     value=False
# )

# if uploaded_files:

#     os.makedirs(
#         "uploads",
#         exist_ok=True
#     )

#     pdf_paths = []

#     for file in uploaded_files:

#         file_path = os.path.join(
#             "uploads",
#             file.name
#         )

#         with open(
#             file_path,
#             "wb"
#         ) as f:

#             f.write(
#                 file.read()
#             )

#         pdf_paths.append(
#             file_path
#         )

#     if st.sidebar.button(
#         "Process PDFs"
#     ):

#         with st.spinner(
#             "Creating Vector Database..."
#         ):

#             vectorstore = create_vectorstore(
#                 pdf_paths
#             )

#             save_vectorstore(
#                 vectorstore
#             )

#         st.sidebar.success(
#             "PDFs Processed Successfully"
#         )

# query = st.text_input(
#     "Enter your question"
# )

# if st.button("Research"):

#     if not query.strip():

#         st.warning(
#             "Please enter a question."
#         )

#     else:

#         state = {
#             "query": query,
#             "plan": "",
#             "research": "",
#             "sources": [],
#             "critic_decision": "",
#             "missing_information": "",
#             "answer": "",
#             "research_attempts": 0,
#             "use_pdf": use_pdf
#         }

#         with st.spinner(
#             "Researching..."
#         ):

#             result = graph.invoke(
#                 state
#             )

#         st.subheader(
#             "Answer"
#         )

#         answer = result["answer"]

#         if "## References" in answer:
#             answer = answer.split("## References")[0].strip()

#         st.markdown(answer)

#         with st.expander(
#             "Sources"
#         ):

#             for source in result["sources"]:

#                 st.write(source)


import os
import streamlit as st

from graph import graph
from rag import (
    create_vectorstore,
    save_vectorstore
)

st.set_page_config(
    page_title="AI Research Assistant",
    layout="wide"
)

st.title("AI Research Assistant")

st.sidebar.header("PDF Knowledge Base")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

use_pdf = st.sidebar.checkbox(
    "Use Uploaded PDFs",
    value=False
)

if uploaded_files:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    pdf_paths = []

    for file in uploaded_files:

        path = os.path.join(
            "uploads",
            file.name
        )

        with open(path, "wb") as f:

            f.write(file.read())

        pdf_paths.append(path)

    if st.sidebar.button("Process PDFs"):

        with st.spinner("Creating vector database..."):

            try:

                vectorstore = create_vectorstore(
                    pdf_paths
                )

                save_vectorstore(
                    vectorstore
                )

                st.sidebar.success(
                    "PDF processing completed."
                )

            except Exception as e:

                st.sidebar.error(str(e))

query = st.text_input(
    "Enter your question"
)

if st.button("Research"):

    if query.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

        state = {

            "query": query,

            "plan": "",

            "research": "",

            "sources": [],

            "critic_decision": "",

            "missing_information": "",

            "answer": "",

            "research_attempts": 0,

            "use_pdf": use_pdf

        }

        try:

            with st.spinner(
                "Researching..."
            ):

                result = graph.invoke(
                    state
                )

            answer = result["answer"]

            if "## References" in answer:

                answer = answer.split(
                    "## References"
                )[0].strip()

            st.subheader(
                "Answer"
            )

            st.markdown(answer)

            if result["sources"]:

                with st.expander(
                    "Sources"
                ):

                    for source in result["sources"]:

                        st.write(source)

        except Exception as e:

            message = str(e)

            if "RateLimitError" in message:

                st.error(
                    "Groq rate limit reached.\n\nPlease wait a while and try again."
                )

            else:

                st.error(message)