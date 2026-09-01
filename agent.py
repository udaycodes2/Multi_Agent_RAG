from dotenv import load_dotenv

from langchain_groq import ChatGroq

from tools import web_search
from rag import search_pdf
from report import create_report

load_dotenv()

llm = ChatGroq(
    model_name="qwen/qwen3.6-27b",
    temperature=0
)

SYSTEM_PROMPT = """
You are an AI Research Assistant.

Rules:

1. Answer only using provided context.
2. If information is missing, clearly state it.
3. Do not hallucinate.
4. Cite evidence whenever possible.
5. Use structured responses.
6. Be concise but informative.
"""


def research_agent(query, memory, vectorstore=None):

    memory_context = memory.get_context()

    pdf_context = ""
    web_context = ""

    sources = []

    if vectorstore:

        pdf_results = search_pdf(
            vectorstore,
            query
        )

        for item in pdf_results:

            pdf_context += f"""
Source File: {item['file']}

Page: {item['page']}

Content:
{item['content']}
"""

            sources.append(
                f"{item['file']} Page {item['page']}"
            )

    web_results = web_search(query)

    for item in web_results:

        web_context += f"""
Title:
{item['title']}

Content:
{item['content']}

URL:
{item['url']}
"""

        sources.append(
            item["url"]
        )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:

{memory_context}

PDF Context:

{pdf_context}

Web Context:

{web_context}

Question:

{query}

Provide:

1. Explanation
2. Key Insights
3. Conclusion

Mention when evidence is insufficient.
"""

    response = llm.invoke(prompt)

    memory.add_message(
        query,
        response.content
    )

    report = create_report(
        question=query,
        answer=response.content,
        sources=sources
    )

    return {
        "answer": response.content,
        "report": report,
        "sources": sources
    }