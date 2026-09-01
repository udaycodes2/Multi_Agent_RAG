---

title: AI Research Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.46.1"
python_version: "3.11"
app_file: app.py
pinned: false
-------------

# 🤖 AI Research Assistant

An intelligent, agent-powered research assistant built with **LangGraph, LangChain, Groq, FAISS, and Streamlit**.

The application can perform **live web research**, analyze **uploaded PDF documents**, retrieve relevant information using **Retrieval-Augmented Generation (RAG)**, and generate structured, source-backed research reports.

---

## ✨ Features

* 🌐 **Live Web Research** using Tavily Search
* 📄 **PDF Question Answering** with RAG
* 🧠 **Agentic Research Workflow** powered by LangGraph
* 📊 **Structured Research Reports**
* 🔍 **Semantic Search** using FAISS vector search
* 📚 **Source Attribution** for research responses
* 📝 **Multi-step Research Planning**
* 💡 **Intelligent Recommendations and Analysis**
* 🖥️ **Interactive Streamlit Interface**
* 📂 Support for **multiple PDF uploads**

---

## 🚀 What Can It Do?

### 🌐 Web Research

Enter any research topic and the assistant performs a multi-step research workflow to gather and analyze information.

The generated report can include:

* Executive Summary
* Key Findings
* Detailed Analysis
* Important Insights
* Recommendations
* Conclusion
* Source References

Example queries:

* *Latest trends in Artificial Intelligence*
* *Compare LangChain and LlamaIndex*
* *Future of autonomous agents*
* *Market analysis of electric vehicles*
* *Impact of generative AI on software development*

---

### 📄 PDF Research

Upload one or more PDF documents and ask questions about their contents.

The system:

1. Extracts text from uploaded PDFs
2. Splits documents into meaningful chunks
3. Converts chunks into vector embeddings
4. Stores embeddings in a FAISS vector database
5. Retrieves the most relevant context
6. Generates a contextual AI response
7. Provides source references

This allows you to ask questions without manually reading through entire documents.

---

## 🏗️ Architecture

### Web Research Pipeline

```text
User Query
    │
    ▼
Planner Agent
    │
    ▼
Web Search (Tavily)
    │
    ▼
Research Aggregation
    │
    ▼
Critic / Evaluation Agent
    │
    ▼
Final Report Generation
    │
    ▼
Response with Sources
```

---

### PDF Research Pipeline

```text
Upload PDF
    │
    ▼
PDF Text Extraction
    │
    ▼
Document Chunking
    │
    ▼
Embedding Generation
    │
    ▼
FAISS Vector Store
    │
    ▼
Similarity Search
    │
    ▼
Relevant Context Retrieval
    │
    ▼
LLM Response
    │
    ▼
Source References
```

---

## 🧰 Tech Stack

### Frontend

* Streamlit

### AI & LLM

* Groq API
* Qwen 3.6 27B

### Agent Framework

* LangChain
* LangGraph

### Retrieval & Vector Search

* FAISS
* HuggingFace Embeddings
* `sentence-transformers/all-MiniLM-L6-v2`

### Web Search

* Tavily Search API

### PDF Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

### Programming Language

* Python 3.11

---

## 📁 Project Structure

```text
AI-Research-Assistant/
│
├── app.py                 # Streamlit application
├── graph.py               # LangGraph agent workflow
├── rag.py                 # RAG and document retrieval logic
├── tools.py               # Search and utility tools
├── requirements.txt       # Project dependencies
│
├── uploads/               # Uploaded PDF documents
├── faiss_index/           # FAISS vector database
│
└── README.md              # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Research-Assistant.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Research-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Make sure you have valid API keys before running the application.

> ⚠️ Never commit your `.env` file or API keys to a public repository.

You can also add the following to your `.gitignore` file:

```text
.env
venv/
__pycache__/
uploads/
faiss_index/
```

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Then open the local URL displayed in your terminal.

---

## 💡 Example Use Cases

The AI Research Assistant can be used for:

* 📚 Research paper summarization
* 🔬 Technical research
* 🤖 AI and technology trend analysis
* 📈 Market research
* 💰 Investment research
* ⚔️ Technology comparisons
* 📄 Technical documentation analysis
* 🧠 Knowledge extraction from PDFs
* 📊 Business and strategy research
* 🛍️ Product comparisons
* 📋 Budget and planning assistance
* 💡 Recommendation generation

---

## 🧠 How the Agent Workflow Works

The application uses an agent-based workflow to improve the quality of research responses.

### 1. Planning

The planner analyzes the user's query and determines the information required.

### 2. Research

Relevant information is collected through web search or document retrieval.

### 3. Aggregation

The retrieved information is combined and organized into useful context.

### 4. Evaluation

The workflow evaluates the collected research and identifies missing or weak information.

### 5. Report Generation

The LLM generates a structured and readable final response with relevant sources.

---

## 🔮 Future Improvements

Planned improvements include:

* 💬 Conversation memory
* 🤝 Multi-agent parallel research
* ⚡ Streaming responses
* 🖼️ Image and chart understanding
* 📌 Improved citation ranking
* 📄 Export research reports as PDF
* 🕒 Persistent chat history
* ☁️ Improved cloud deployment
* 🔐 User authentication
* 🗂️ Support for additional document formats
* 📊 Automatic data visualization
* 🔎 Advanced research filtering

---

## 🎯 Project Goals

The goal of this project is to demonstrate how modern AI technologies can be combined to build a practical research assistant using:

* Large Language Models
* Agentic workflows
* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* Live web search
* Interactive user interfaces

---

## 🤝 Contributing

Contributions, ideas, and improvements are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Open a pull request

---

## 📜 License

This project is intended for **educational, learning, and portfolio purposes**.

If you plan to use this project commercially, make sure to review the licenses and terms of the third-party libraries, APIs, models, and services used in the project.

---

## ⭐ Support

If you found this project useful, consider giving the repository a **star ⭐**.

It helps others discover the project and motivates further improvements.

---

<p align="center">
  Built with ❤️ using Python, LangChain, LangGraph, Groq, FAISS, and Streamlit.
</p>
