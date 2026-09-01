import os

from rag import create_vectorstore

pdfs = []

for file in os.listdir("uploads"):

    if file.endswith(".pdf"):

        pdfs.append(
            os.path.join(
                "uploads",
                file
            )
        )

print("\nPDFs Found:\n")

for pdf in pdfs:
    print(pdf)

vectorstore = create_vectorstore(pdfs)

vectorstore.save_local("faiss_index")

print("\nFAISS index created successfully")