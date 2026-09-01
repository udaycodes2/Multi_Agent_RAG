# import os
# from typing import TypedDict, List
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph, START, END

# from tools import web_search
# from rag import search_pdf

# load_dotenv()

# llm = ChatGroq(
#     model_name="llama-3.3-70b-versatile",
#     temperature=0
# )

# class AgentState(TypedDict):
#     query: str
#     plan: str
#     research: str
#     sources: List[str]
#     critic_decision: str
#     missing_information: str
#     answer: str
#     research_attempts: int
#     use_pdf: bool

# def planner_node(state: AgentState):

#     prompt = f"""
# You are a research planner.

# Question:
# {state["query"]}

# Create a research plan.

# Rules:

# - Identify the major subtopics.
# - Identify information needed.
# - Do not answer.
# - Maximum 6 bullet points.
# """

#     response = llm.invoke(prompt)

#     state["plan"] = response.content

#     return state


# def generate_search_queries(state: AgentState):

#     prompt = f"""
# You are an expert search strategist.

# Question:
# {state["query"]}

# Research Plan:
# {state["plan"]}

# Generate 6 highly specific web search queries.

# Rules:

# - Focus on recent information.
# - Include years when useful.
# - Avoid generic searches.
# - One query per line.
# - No numbering.
# """

#     response = llm.invoke(prompt)

#     queries = []

#     for line in response.content.split("\n"):

#         line = line.strip()

#         if line:
#             queries.append(line)

#     return queries[:6]

# def reflection_node(state: AgentState):

#     prompt = f"""
# You are a reflection agent.

# Question:

# {state["query"]}

# Missing Information:

# {state["missing_information"]}

# Generate 3 focused search queries
# to obtain the missing information.

# Rules:
# - One query per line
# - No numbering
# - Keep each query short
# """

#     response = llm.invoke(prompt)

#     state["plan"] = response.content

#     return state


# def research_node(state: AgentState):

#     state["research_attempts"] += 1

#     research_text = state["research"]
#     sources = state["sources"]

#     pdf_chunks = []

#     if (
#         state["use_pdf"]
#         and state["research_attempts"] == 1
#     ):

#         try:

#             pdf_chunks = search_pdf(
#                 state["query"]
#             )

#         except Exception as e:

#             print(
#                 f"PDF Search Failed: {e}"
#             )

#             pdf_chunks = []

#         for chunk in pdf_chunks:

#             research_text += f"""

# SOURCE: PDF:{chunk["file"]} Page:{chunk["page"]}

# CONTENT:
# {chunk["content"]}

# """

#             sources.append(
#                 f'PDF:{chunk["file"]} Page:{chunk["page"]}'
#             )

#     if state["research_attempts"] == 1:

#         queries = generate_search_queries(
#             state
#         )

#     else:

#         queries = []

#         for line in state["plan"].split("\n"):

#             line = line.strip()

#             if line:
#                 queries.append(line)

#     print("\nSEARCH QUERIES:\n")

#     trusted_domains = [
#     ".gov",
#     ".edu",
#     "openai.com",
#     "anthropic.com",
#     "google.com",
#     "deepmind.google",
#     "microsoft.com",
#     "stanford.edu",
#     "mit.edu",
#     "ibm.com",
#     "mckinsey.com",
#     "gartner.com",
#     "deloitte.com",
#     "pwc.com",
#     "forbes.com",
#     "reuters.com",
#     "techcrunch.com",
#     "nvidia.com",
#     "aws.amazon.com"
#     ]
    
#     blocked_domains = [
#         "instagram.com",
#         "youtube.com",
#         "pinterest.com",
#         "linkedin.com",
#         "facebook.com",
#         "tiktok.com"
#     ]

#     seen_urls = set(sources)

#     all_results = []

#     for q in queries:

#         print(q)

#         try:

#             web_results = web_search(q)

#             query_words = set(
#                 q.lower().split()
#             )

#             for item in web_results:

#                 title = item.get(
#                     "title",
#                     ""
#                 )

#                 content = item.get(
#                     "content",
#                     ""
#                 )

#                 url = item.get(
#                     "url",
#                     ""
#                 )

#                 if not url:
#                     continue

#                 if len(content.strip()) < 150:
#                     continue

#                 if url in seen_urls:
#                     continue

#                 if any(
#                     domain in url.lower()
#                     for domain in blocked_domains
#                 ):
#                     continue

#                 score = 0

#                 text = (
#                     title +
#                     " " +
#                     content[:1500]
#                 ).lower()

#                 query_words = [
#                     word
#                     for word in q.lower().split()
#                     if len(word) > 3
#                 ]

#                 matches = 0

#                 for word in query_words:

#                     if word in text:
#                         matches += 1

#                 score += matches * 4

#                 coverage = matches / max(
#                     len(query_words),
#                     1
#                 )

#                 score += int(
#                     coverage * 20
#                 )

#                 all_results.append(
#                     {
#                         "url": url,
#                         "title": title,
#                         "content": content[:2000],
#                         "score": score
#                     }
#                 )

#                 seen_urls.add(url)

#         except Exception as e:

#             print(
#                 f"Search Failed: {q}"
#             )

#             print(e)

#     all_results.sort(
#         key=lambda x: x["score"],
#         reverse=True
#     )

#     all_results = all_results[:12]

#     for item in all_results:

#         research_text += f"""

# SOURCE: {item["url"]}

# TITLE:
# {item["title"]}

# CONTENT:
# {item["content"]}

# """

#         sources.append(
#             item["url"]
#         )

#     state["research"] = research_text

#     state["sources"] = list(
#         dict.fromkeys(sources)
#     )

#     print(
#         f"\nResearch Sources: {len(state['sources'])}"
#     )

#     print(
#         f"Research Length: {len(research_text)}"
#     )

#     print(
#         f"Attempt: {state['research_attempts']}"
#     )

#     return state

# def critic_node(state: AgentState):

#     prompt = f"""
# You are a strict research reviewer.

# Question:
# {state["query"]}

# Research:
# {state["research"][:7000]}

# Determine whether the research is sufficient.

# Only answer YES if:

# - Main question is directly answered.
# - At least 5 relevant sources exist.
# - Research is specifically about the user question.
# - Important aspects are covered.
# - Evidence is not generic.
# - Sources are not repetitive.
# Answer exactly:

# DECISION: YES

# MISSING:
# None

# OR

# DECISION: NO

# MISSING:
# - item
# - item
# """
#     response = llm.invoke(prompt)

#     output = response.content.strip()

#     if "DECISION: YES" in output:
#         state["critic_decision"] = "YES"
#     else:
#         state["critic_decision"] = "NO"

#     if "MISSING:" in output:
#         state["missing_information"] = (
#             output.split("MISSING:")[1].strip()
#         )
#     else:
#         state["missing_information"] = ""

#     return state


# def writer_node(state: AgentState):

#     prompt = f"""
# You are a senior research analyst.

# Question:
# {state["query"]}

# Research:
# {state["research"][:8000]}

# Rules:

# 1. Use ONLY provided research.

# 2. Do not invent facts.

# 3. Ignore irrelevant research.

# 4. Focus on answering the user's question directly.

# 5. If the question asks for:

#    - recommendation
#    - strategy
#    - planning
#    - decision making
#    - comparison

#    then provide a direct recommendation.

# 6. Do not repeat information.

# 7. Prefer concrete numbers,
#    statistics,
#    costs,
#    dates,
#    trends,
#    recommendations.

# 8. If research is insufficient,
#    explicitly say so.

# Output:

# ## Executive Summary

# 2-4 paragraphs.

# ## Key Findings

# Bullet points.

# ## Detailed Analysis

# Detailed explanation.

# ## Conclusion

# Direct final answer.
# """

#     response = llm.invoke(prompt)

#     answer = response.content.strip()

#     trusted_sources = []

#     for source in state["sources"]:

#         if source.startswith("PDF:"):
#             continue

#         trusted_sources.append(source)

#         if len(trusted_sources) == 5:
#             break

#     if trusted_sources:

#         answer += "\n\n## References\n\n"

#         for source in trusted_sources:

#             answer += f"- {source}\n"

#     state["answer"] = answer

#     return state

# def route_after_critic(state: AgentState):

#     print(
#         f"Routing -> "
#         f"{state['critic_decision']} "
#         f"Attempt={state['research_attempts']}"
#     )

#     if state["critic_decision"] == "YES":

#         print(
#             "Research approved by critic."
#         )

#         return "writer"

#     if state["research_attempts"] < 2:

#         print(
#             "Research incomplete. "
#             "Starting reflection cycle."
#         )

#         return "reflection"

#     print(
#         "Maximum attempts reached. "
#         "Proceeding with available research."
#     )

#     return "writer"


# graph_builder = StateGraph(AgentState)

# graph_builder.add_node(
#     "planner",
#     planner_node
# )

# graph_builder.add_node(
#     "research",
#     research_node
# )

# graph_builder.add_node(
#     "critic",
#     critic_node
# )

# graph_builder.add_node(
#     "reflection",
#     reflection_node
# )

# graph_builder.add_node(
#     "writer",
#     writer_node
# )

# graph_builder.add_edge(
#     START,
#     "planner"
# )

# graph_builder.add_edge(
#     "planner",
#     "research"
# )

# graph_builder.add_edge(
#     "research",
#     "critic"
# )

# graph_builder.add_edge(
#     "reflection",
#     "research"
# )

# graph_builder.add_conditional_edges(
#     "critic",
#     route_after_critic,
#     {
#         "reflection": "reflection",
#         "writer": "writer"
#     }
# )

# graph_builder.add_edge(
#     "writer",
#     END
# )

# graph = graph_builder.compile()


# if __name__ == "__main__":

#     state = {
#         "query": "Build a house in Delhi with 80 lakh",
#         "plan": "",
#         "research": "",
#         "sources": [],
#         "critic_decision": "",
#         "missing_information": "",
#         "answer": "",
#         "research_attempts": 0,
#         "use_pdf" : bool
#     }

#     result = graph.invoke(state)

#     print("\nPLAN:\n")
#     print(result["plan"])

#     print("\nCRITIC:\n")
#     print(result["critic_decision"])

#     print("\nMISSING INFORMATION:\n")
#     print(result["missing_information"])

#     print("\nATTEMPTS:\n")
#     print(result["research_attempts"])

#     print("\nSOURCES:\n")
#     for source in result["sources"]:
#         print(source)

#     print("\nANSWER:\n")
#     print(result["answer"])


# #KGAT_02bef35dc77bbe6ffe5b543d04a0eff7

import os
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from tools import web_search
from rag import search_pdf

load_dotenv()

llm = ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0
)


class AgentState(TypedDict):
    query: str
    plan: str
    research: str
    sources: List[str]

    critic_decision: str
    missing_information: str

    answer: str

    research_attempts: int
    use_pdf: bool

def planner_node(state: AgentState):

    prompt = f"""
You are an expert research planner.

User Question:
{state["query"]}

Your task is ONLY to plan the research.

Instructions:

- Break the question into the major information required.
- Think like an analyst.
- Identify all important aspects.
- Keep the plan concise.
- Maximum 6 bullet points.
- Do NOT answer the question.
"""

    response = llm.invoke(prompt)

    state["plan"] = response.content.strip()

    return state


def generate_search_queries(state: AgentState):

    prompt = f"""
You are an expert web researcher.

Question:
{state["query"]}

Research Plan:
{state["plan"]}

Generate HIGH QUALITY Google-style search queries.

Rules:

- Generate exactly 5 queries.
- Each query should search ONE aspect.
- Include years where useful.
- Include locations where relevant.
- Prefer official reports, statistics and reliable sources.
- Avoid vague queries.
- No numbering.
- One query per line.
"""

    response = llm.invoke(prompt)

    queries = []

    for line in response.content.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = line.lstrip("-•1234567890. ")

        if len(line) > 5:
            queries.append(line)

    return queries[:5]


def reflection_node(state: AgentState):

    prompt = f"""
You are improving an incomplete research report.

Original Question:
{state["query"]}

The research reviewer identified these missing areas:

{state["missing_information"]}

Generate focused search queries ONLY for the missing information.

Rules:

- Generate exactly 3 queries.
- One query per line.
- No numbering.
- Avoid repeating previous searches.
- Keep queries concise.
"""

    response = llm.invoke(prompt)

    state["plan"] = response.content.strip()

    return state

def research_node(state: AgentState):

    state["research_attempts"] += 1

    research_text = state["research"]
    sources = state["sources"]

    if state["research_attempts"] == 1:

        if state["use_pdf"]:

            try:

                pdf_chunks = search_pdf(
                    state["query"]
                )

            except Exception as e:

                print(e)

                pdf_chunks = []

            for chunk in pdf_chunks:

                research_text += f"""

SOURCE: PDF:{chunk["file"]} Page:{chunk["page"]}

CONTENT:
{chunk["content"]}

"""

                sources.append(
                    f'PDF:{chunk["file"]} Page:{chunk["page"]}'
                )

        queries = generate_search_queries(state)

    else:

        queries = []

        for line in state["plan"].split("\n"):

            line = line.strip()

            if line:

                queries.append(line)

    print("\nSEARCH QUERIES\n")

    trusted_domains = [

        ".gov",
        ".edu",

        "openai.com",
        "anthropic.com",
        "google.com",
        "deepmind.google",
        "microsoft.com",

        "stanford.edu",
        "mit.edu",

        "nature.com",
        "science.org",
        "arxiv.org",

        "who.int",
        "worldbank.org",
        "oecd.org",

        "ibm.com",
        "mckinsey.com",

    ]

    blocked_domains = [

        "youtube.com",
        "instagram.com",
        "facebook.com",
        "linkedin.com",
        "tiktok.com",
        "pinterest.com"

    ]

    seen_urls = set(sources)

    all_results = []

    for query in queries:

        print(query)

        try:

            results = web_search(
                query,
                max_results=5
            )

        except Exception as e:

            print(e)

            continue

        query_words = set(
            query.lower().split()
        )

        for item in results:

            url = item.get("url", "")
            title = item.get("title", "")
            content = item.get("content", "")

            if not url:
                continue

            if url in seen_urls:
                continue

            if any(
                x in url.lower()
                for x in blocked_domains
            ):
                continue

            if len(content) < 300:
                continue

            score = 0

            text = (
                title +
                " " +
                content
            ).lower()

            for word in query_words:

                if len(word) > 3 and word in text:

                    score += 2

            if any(
                d in url.lower()
                for d in trusted_domains
            ):

                score += 6

            score += min(
                len(content) // 700,
                4
            )

            all_results.append(

                {

                    "score": score,

                    "url": url,

                    "title": title,

                    "content": content[:1800]

                }

            )

            seen_urls.add(url)

    all_results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    final_results = all_results[:8]

    for item in final_results:

        research_text += f"""

SOURCE: {item["url"]}

TITLE:
{item["title"]}

CONTENT:
{item["content"]}

"""

        sources.append(item["url"])

    state["research"] = research_text

    state["sources"] = list(
        dict.fromkeys(sources)
    )

    print(
        f"\nResearch Length : {len(research_text)}"
    )

    print(
        f"Sources : {len(state['sources'])}"
    )

    print(
        f"Attempt : {state['research_attempts']}"
    )

    return state

def critic_node(state: AgentState):

    prompt = f"""
You are a senior research reviewer.

Question:
{state["query"]}

Research:
{state["research"][:7000]}

Evaluate ONLY whether the available research is sufficient.

Answer YES only if:

- The main question is answered.
- Important facts are present.
- The research is reliable.
- No major information is missing.

Return EXACTLY in this format:

DECISION: YES

MISSING:
None

OR

DECISION: NO

MISSING:
- point 1
- point 2
"""

    response = llm.invoke(prompt)

    output = response.content.strip()

    if "DECISION: YES" in output:
        state["critic_decision"] = "YES"
    else:
        state["critic_decision"] = "NO"

    if "MISSING:" in output:
        state["missing_information"] = output.split(
            "MISSING:"
        )[1].strip()
    else:
        state["missing_information"] = ""

    return state


def writer_node(state: AgentState):

    prompt = f"""
You are a senior research analyst.

Question:
{state["query"]}

Research:
{state["research"][:9000]}

Rules:

- Use ONLY the provided research.
- Never invent facts.
- Ignore irrelevant information.
- Merge duplicate information.
- Use concrete numbers whenever available.
- Write clearly and professionally.

If the user asks for:

- recommendation
- planning
- strategy
- comparison

provide a clear recommendation.

If the research is incomplete,
say what information could not be verified.

Output Format:

## Executive Summary

2-3 short paragraphs.

## Key Findings

Bullet points.

## Detailed Analysis

Well structured explanation.

## Conclusion

Clear final answer.
"""

    response = llm.invoke(prompt)

    state["answer"] = response.content.strip()

    return state


def route_after_critic(state: AgentState):

    print(
        f"Critic Decision : {state['critic_decision']}"
    )

    print(
        f"Research Attempt : {state['research_attempts']}"
    )

    if state["critic_decision"] == "YES":

        print("Research Approved")

        return "writer"

    if state["research_attempts"] < 2:

        print("Running Reflection")

        return "reflection"

    print("Maximum Attempts Reached")

    return "writer"

graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "planner",
    planner_node
)

graph_builder.add_node(
    "research",
    research_node
)

graph_builder.add_node(
    "reflection",
    reflection_node
)

graph_builder.add_node(
    "critic",
    critic_node
)

graph_builder.add_node(
    "writer",
    writer_node
)

graph_builder.add_edge(
    START,
    "planner"
)

graph_builder.add_edge(
    "planner",
    "research"
)

graph_builder.add_edge(
    "research",
    "critic"
)

graph_builder.add_edge(
    "reflection",
    "research"
)

graph_builder.add_conditional_edges(
    "critic",
    route_after_critic,
    {
        "reflection": "reflection",
        "writer": "writer"
    }
)

graph_builder.add_edge(
    "writer",
    END
)

graph = graph_builder.compile()


if __name__ == "__main__":

    state = {

        "query": "Summarize the Attention Is All You Need paper.",

        "plan": "",

        "research": "",

        "sources": [],

        "critic_decision": "",

        "missing_information": "",

        "answer": "",

        "research_attempts": 0,

        "use_pdf": False

    }

    result = graph.invoke(state)

    print("\n==============================")
    print("PLAN")
    print("==============================")
    print(result["plan"])

    print("\n==============================")
    print("CRITIC")
    print("==============================")
    print(result["critic_decision"])

    print("\n==============================")
    print("MISSING INFORMATION")
    print("==============================")
    print(result["missing_information"])

    print("\n==============================")
    print("RESEARCH ATTEMPTS")
    print("==============================")
    print(result["research_attempts"])

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    for source in result["sources"]:

        print(source)

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    print(result["answer"])