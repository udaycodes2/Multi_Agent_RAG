# 🚀 Advanced Agentic RAG 

A production-inspired **Multi-Agent Retrieval-Augmented Generation
(RAG)** application built using **LangChain**, **LangGraph**,
**Streamlit**, **ChromaDB**, and **Groq LLMs**.

The system leverages a modular, agent-based architecture to
intelligently retrieve, validate, and generate reliable responses from
both private knowledge sources and real-time web data.

Unlike traditional RAG applications, this project introduces **dynamic
query routing, self-correcting retrieval, fact verification, and safety
evaluation**, creating a more accurate and robust AI assistant.

------------------------------------------------------------------------

# ✨ Features

## 🤖 Multi-Agent Architecture

The application consists of specialized AI agents:

-   **Router Agent** -- Determines the best workflow for each query.
-   **Retriever Agent** -- Retrieves relevant information from the
    knowledge base.
-   **Query Reformulator** -- Rewrites unclear queries for better
    retrieval.
-   **Web Search Agent** -- Retrieves real-time information using
    Tavily.
-   **Synthesizer Agent** -- Combines information from multiple sources.
-   **Response Generator** -- Produces context-aware answers using Groq
    LLMs.
-   **Fact Checker** -- Verifies factual claims using live web search.
-   **Safety Checker** -- Detects unsafe or harmful content.
-   **Clarifier Agent** -- Requests additional user input when
    necessary.

------------------------------------------------------------------------

# 📚 Hybrid Knowledge Retrieval

Supports multiple knowledge sources:

-   PDF
-   DOCX
-   TXT
-   Website URLs

Documents are embedded into **ChromaDB** for semantic retrieval, while
external information is fetched dynamically through Tavily Search.

------------------------------------------------------------------------

# 🔄 Workflow

``` text
                User
                  │
                  ▼
           Router Agent
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
Retriever Agent        Web Search Agent
      │                       │
      └───────────┬───────────┘
                  ▼
          Synthesizer Agent
                  ▼
        Response Generator
                  ▼
          Fact Checker
                  ▼
         Safety Checker
                  ▼
              Final Answer
```

------------------------------------------------------------------------

# 🛠️ Tech Stack

### Frontend

-   Streamlit

### AI Framework

-   LangChain
-   LangGraph

### LLM

-   Groq

### Embeddings

-   Google Generative AI Embeddings

### Vector Database

-   ChromaDB

### Search

-   Tavily Search API

------------------------------------------------------------------------

# ⚙️ Installation

``` bash
git clone https://github.com/Tirth1411/advanced-agentic-rag.git
cd advanced-agentic-rag
```

Create a virtual environment:

``` bash
python -m venv venv
```

Windows:

``` bash
venv\Scripts\activate
```

Linux / macOS:

``` bash
source venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🔑 API Keys

Create:

``` text
.streamlit/secrets.toml
```

Add:

``` toml
LANGCHAIN_API_KEY = "YOUR_KEY"
TAVILY_API_KEY = "YOUR_KEY"
GOOGLE_API_KEY = "YOUR_KEY"
GROQ_API_KEY = "YOUR_KEY"
```

------------------------------------------------------------------------

# ▶️ Run

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

# ⚙️ Configurable Parameters

-   Chunk Size
-   Chunk Overlap
-   Retriever Top-K
-   LLM Temperature

------------------------------------------------------------------------

# 🚀 Future Improvements

-   FastAPI backend
-   Docker support
-   Authentication
-   Chat history database
-   CI/CD pipeline
-   Hybrid Search (BM25 + Vector Search)
-   LangSmith Observability
-   Cloud Deployment


------------------------------------------------------------------------

# 🙏 Acknowledgements

-   LangChain
-   LangGraph
-   Streamlit
-   Groq
-   Google Generative AI
-   Tavily
-   ChromaDB
