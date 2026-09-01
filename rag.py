# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# import os

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# vectorstore = None


# def create_vectorstore(pdf_paths):

#     all_docs = []

#     for pdf_path in pdf_paths:

#         if not os.path.exists(pdf_path):
#             continue

#         loader = PyPDFLoader(pdf_path)

#         docs = loader.load()

#         filename = os.path.basename(pdf_path)

#         for doc in docs:
#             doc.metadata["source_file"] = filename

#         all_docs.extend(docs)

#     if not all_docs:
#         raise ValueError("No PDF documents found")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=100
#     )

#     chunks = splitter.split_documents(all_docs)

#     vectorstore = FAISS.from_documents(
#         chunks,
#         embeddings
#     )

#     return vectorstore


# def save_vectorstore(vectorstore, path="faiss_index"):

#     vectorstore.save_local(path)


# def load_vectorstore(path="faiss_index"):

#     if not os.path.exists(path):
#         raise FileNotFoundError(
#             f"FAISS index folder '{path}' not found"
#         )

#     return FAISS.load_local(
#         path,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )


# def search_pdf(query):

#     global vectorstore

#     try:

#         if vectorstore is None:
#             vectorstore = load_vectorstore()

#     except Exception:
#         return []

#     results = vectorstore.similarity_search_with_score(
#         query,
#         k=5
#     )

#     final_results = []

#     for doc, score in results:

#         if score > 0.8:
#             continue

#         content = doc.page_content.strip()

#         if len(content) < 150:
#             continue

#         final_results.append(
#             {
#                 "content": content,
#                 "page": doc.metadata.get("page", 0) + 1,
#                 "file": doc.metadata.get(
#                     "source_file",
#                     "Unknown"
#                 ),
#                 "score": round(score, 3)
#             }
#         )

#     return final_results

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import os

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = None


def create_vectorstore(pdf_paths):

    all_docs = []

    for pdf_path in pdf_paths:

        if not os.path.exists(pdf_path):
            continue

        loader = PyPDFLoader(pdf_path)

        docs = loader.load()

        filename = os.path.basename(pdf_path)

        for doc in docs:

            doc.metadata["source_file"] = filename

        all_docs.extend(docs)

    if not all_docs:

        raise ValueError("No PDF documents found.")

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=200,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )

    chunks = splitter.split_documents(all_docs)

    vectorstore = FAISS.from_documents(

        chunks,

        embeddings

    )

    return vectorstore


def save_vectorstore(vectorstore, path="faiss_index"):

    vectorstore.save_local(path)


def load_vectorstore(path="faiss_index"):

    if not os.path.exists(path):

        raise FileNotFoundError(
            "Vectorstore not found."
        )

    return FAISS.load_local(

        path,

        embeddings,

        allow_dangerous_deserialization=True

    )


def search_pdf(query):

    global vectorstore

    try:

        if vectorstore is None:

            vectorstore = load_vectorstore()

    except Exception:

        return []

    retriever = vectorstore.as_retriever(

        search_type="mmr",

        search_kwargs={

            "k": 8,

            "fetch_k": 20,

            "lambda_mult": 0.6

        }

    )

    docs = retriever.invoke(query)

    final_results = []

    seen_pages = set()

    for doc in docs:

        page = doc.metadata.get("page", 0) + 1

        if page in seen_pages:
            continue

        seen_pages.add(page)

        content = doc.page_content.strip()

        if len(content) < 200:
            continue

        final_results.append(

            {

                "content": content,

                "page": page,

                "file": doc.metadata.get(

                    "source_file",

                    "Unknown"

                )

            }

        )

    return final_results