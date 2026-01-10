# 🛒 E-Commerce Product Assistant using RAG & Real-Time Data

## 📌 Overview
This project implements an **AI-powered e-commerce product assistant** capable of answering user queries using both **static product data** and **real-time information** from live sources. The system is built using **Retrieval-Augmented Generation (RAG)** combined with **agent-based reasoning**, enabling accurate, up-to-date, and context-aware product insights.

The assistant is designed to support intelligent product discovery, comparison, and decision-making in real-world e-commerce scenarios.

---

## 🎯 Key Capabilities
- Conversational-AI for product search and Q&A  
- Integration of static catalogs with live web scraping using beautifulsoup4, Selenium WebDriver 
- Multi-step reasoning using agent-based workflows using langchain and MCP
- Web Search feedback loop for realtime information retrival 
- Production-ready backend and deployment pipeline using github actions, and AWS ECR+EKS

---

## 🧠 System Architecture

The system follows an **agentic RAG architecture**:

- **Static Knowledge Base** – Indexed product catalogs and metadata  
- **Live Data Retrieval** – Web scraping and API-based data fetching  
- **Agent Orchestration** – Coordinates retrieval, reasoning, and response generation  
- **RAG Pipeline** – Grounds LLM responses using retrieved product context  
- **Response Generator** – Produces concise, user-friendly answers  
- **Backend Services** – API-driven execution and monitoring  

The architecture supports extensibility for new data sources and reasoning tools.

---

## 🔧 Core Technologies
- **LLMs:** Large Language Models for conversational responses  
- **RAG Framework:** Retrieval-Augmented Generation pipelines  
- **Agents Workflow:** Agent orchestration and tool calling with Langgraph
- **Embeddings:** langchain-google-genai, langchain-astradb (semantic search)  
- **Vector Stores:** AstraDB  
- **Backend:** FastAPI, Streamlit, Ragas(evaluation)
- **Deployment:** Docker, CI/CD, Cloud-ready infrastructure using GithubActions + ECR + EKS

---

## 📂 Workflow
1. User submits a product-related query  
2. Agent determines whether static or live data is required  
3. Relevant product data is retrieved and indexed context is fetched  
4. Live data sources are queried when needed  
5. LLM generates a grounded, contextual response  
6. Final answer is returned to the user  

---

## 📈 Use Cases
- Webscraping of web based programming documentation for CAE specific tools (Altair, Ansys, Abaqus, LS-Dyna) for generative AI based agentic coding (Ongoing)
- Product discovery and recommendation  
- Feature comparison and specification lookup  
- Price and availability insights  
- Customer support automation  
- Intelligent shopping assistants  

---

## ✅ Key Design Principles
- **Accuracy:** Responses grounded in retrieved product data  
- **Freshness:** Live data integration for up-to-date answers  
- **Scalability:** Designed for real-time user interactions  
- **Modularity:** Easy integration of new data sources or tools  

---

## 🚀 Future Enhancements
- Personalization using user preferences  
- Multi-vendor and multi-platform support  
- Product ranking and recommendation logic  
- UI enhancements for interactive shopping experiences  

