# import os

# from dotenv import load_dotenv
# from tavily import TavilyClient

# load_dotenv()

# client = TavilyClient(
#     api_key=os.getenv("TAVILY_API_KEY")
# )

# def web_search(query, max_results=5):

#     try:

#         response = client.search(
#             query=query,
#             max_results=max_results,
#             search_depth="advanced",
#             include_answer=False,
#             include_raw_content=True
#         )

#         results = []

#         blocked_domains = [
#             "instagram.com",
#             "youtube.com",
#             "pinterest.com",
#             "facebook.com",
#             "linkedin.com",
#             "tiktok.com"
#         ]

#         for item in response.get(
#             "results",
#             []
#         ):

#             url = item.get(
#                 "url",
#                 ""
#             )

#             if not url:
#                 continue

#             if any(
#                 domain in url.lower()
#                 for domain in blocked_domains
#             ):
#                 continue

#             content = (
#                 item.get(
#                     "raw_content"
#                 )
#                 or item.get(
#                     "content"
#                 )
#                 or ""
#             )

#             if len(content.strip()) < 200:
#                 continue

#             results.append(
#                 {
#                     "title": item.get(
#                         "title",
#                         ""
#                     ),
#                     "content": content[:4000],
#                     "url": url
#                 }
#             )

#         return results

#     except Exception as e:

#         print(
#             f"Web Search Error: {e}"
#         )

#         return []


import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def web_search(query, max_results=5):

    try:

        response = client.search(

            query=query,

            max_results=max_results,

            search_depth="advanced",

            topic="general",

            include_answer=False,

            include_raw_content=True,

            include_images=False

        )

    except Exception as e:

        print(f"Web Search Error: {e}")

        return []

    blocked_domains = [

        "youtube.com",
        "instagram.com",
        "facebook.com",
        "linkedin.com",
        "tiktok.com",
        "pinterest.com",

        "quora.com",
        "reddit.com",

        "medium.com"

    ]

    results = []

    seen_urls = set()

    for item in response.get("results", []):

        url = item.get("url", "")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        if any(
            domain in url.lower()
            for domain in blocked_domains
        ):
            continue

        title = item.get(
            "title",
            ""
        ).strip()

        content = (

            item.get("raw_content")

            or item.get("content")

            or ""

        ).strip()

        if len(content) < 300:
            continue

        results.append(

            {

                "title": title,

                "content": content[:3500],

                "url": url

            }

        )

    return results