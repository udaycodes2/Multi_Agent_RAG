# # from rag import create_vectorstore
# # from rag import search_pdf

# # vectorstore = create_vectorstore(
# #     [
# #         "uploads/budget.pdf"
# #     ]
# # )

# # results = search_pdf(
# #     vectorstore,
# #     "benefits for middle class"
# # )

# # for r in results:

# #     print("\n")

# #     print(r["file"])

# #     print(r["page"])

# #     print(r["content"][:200])

# from tools import web_search

# results = web_search(
#     "Latest AI trends"
# )

# for r in results:

#     print("\n")

#     print(r["title"])

#     print(r["url"])

# from memory import ConversationMemory

# memory = ConversationMemory()

# memory.add_message(
#     "What is GDP?",
#     "GDP is total value of goods and services."
# )

# memory.add_message(
#     "What is inflation?",
#     "Inflation is rise in prices."
# )

# print(memory.get_context())

# from report import create_report

# report = create_report(
#     question="Latest AI Trends",

#     answer="AI Agents and RAG are growing rapidly.",

#     sources=[
#         "abc.com",
#         "xyz.com",
#         "abc.com"
#     ]
# )

# print(report)

from rag import create_vectorstore
from memory import ConversationMemory
from agent import research_agent

pdf_paths = [
    "uploads/budget.pdf"
]

vectorstore = create_vectorstore(pdf_paths)

memory = ConversationMemory()

result = research_agent(
    query="What are the benefits for the middle class in this budget?",
    memory=memory,
    vectorstore=vectorstore
)

print("\nANSWER:\n")
print(result["answer"])

print("\nSOURCES:\n")
for source in result["sources"]:
    print(source)

print("\nREPORT:\n")
print(result["report"])