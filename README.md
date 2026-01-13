Company Policy Agentic Q&A System (RAG-based AI Agent)
🔍 Overview
This project implements an Agentic Retrieval-Augmented Generation (RAG) system that answers user queries related to internal company documents such as policies and guidelines.
The system intelligently decides whether:
•	A query can be answered directly using an LLM, or
•	Relevant information needs to be retrieved from internal documents before generating a response.
The application is deployed on Azure App Service and exposed via a public API using FastAPI.
________________________________________
🧠 Architecture Overview
High-Level Flow:
User Query
   ↓
FastAPI (/ask)
   ↓
Agent (ReAct Pattern)
   ↓
Tool Decision
   ├── Direct LLM Answer
   └── Policy Retriever Tool (RAG)
           ↓
      FAISS Vector Store
           ↓
      Relevant Document Chunks
           ↓
Azure OpenAI (Chat Model)
   ↓
Final Answer + Source Documents
________________________________________
🛠 Tech Stack
Core Technologies
•	Python 3.10
•	FastAPI – Backend API
•	LangChain (Agent + RAG)
•	FAISS – Vector database for embeddings
•	Azure OpenAI
o	Chat Model (e.g., GPT-4o-mini)
o	Embedding Model (text-embedding-3-large)
Deployment
•	Azure App Service (Linux)
•	Azure App Service Plan (F1)
•	GitHub Actions (CI/CD)
________________________________________
📂 Project Structure
Company-Policy-Agentic-Q-A-System/
│
├── main.py                         # FastAPI + Agent logic
├── requirements.txt         # Python dependencies
├── data/
│   └── Company_Policy_Handbook.pdf
│   └── India-Leaves and Holiday Policy-042624
├── .env                               # Environment variable template
├── README.md                # Project documentation
└── .github/
    └── workflows/
        └── azure-webapps.yml
________________________________________
🧩 Features Implemented (Mapped to Assignment Tasks)
✅ Task 1: AI Agent Development
•	Agent built using ReAct pattern
•	Uses tool calling to decide:
o	Direct LLM response OR
o	Document retrieval via RAG
•	Session-based memory using ConversationBufferMemory
•	Prompt engineered to ensure structured and grounded responses
________________________________________
✅ Task 2: Retrieval-Augmented Generation (RAG)
•	Sample documents provided (Company Policy PDF, Leaves and Holiday Policy)
•	Documents split into chunks
•	Embeddings generated using Azure OpenAI Embedding model
•	Stored in FAISS
•	Relevant chunks retrieved and injected into LLM context
________________________________________
✅ Task 3: Backend API
Endpoint
POST /ask
Request
{
  "query": "What are the company policies?",
  "session_id": "optional-session-id"
}
Response
{
  "answer": "The company has several key policies...",
  "source": ["data/Company_Policy_Handbook.pdf"]
}
________________________________________
✅ Task 4: Azure Deployment
•	Deployed on Azure App Service (Linux)
•	Uses Azure OpenAI
•	Secrets managed via environment variables
•	Publicly accessible API
🔗 Live API Docs
https://agentic-rag-policy-api-aqb5b9b6gmg8gzgk.centralindia-01.azurewebsites.net/docs
________________________________________
⚙️ Setup Instructions
🔹 Local Setup
1.	Clone the repository:
git clone https://github.com/amitksingh2103/Company-Policy-Agentic-Q-A-System.git
cd Company-Policy-Agentic-Q-A-System
2.	Create virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3.	Install dependencies:
pip install -r requirements.txt
4.	Configure environment variables:
cp .env.example .env
5.	Run the app:
uvicorn main:app --host 0.0.0.0 --port 8000
6.	Open:
http://localhost:8000/docs
________________________________________
🔹 Azure Deployment (Code-Based)
•	Azure App Service (Linux, Python 3.10)
•	GitHub Actions used for CI/CD
•	Environment variables configured in Azure → Configuration
________________________________________
Dockerization 
The application has also been fully containerized using Docker to demonstrate production readiness and portability.
Docker Image
•	Docker Hub Repository:
https://hub.docker.com/r/amitksingh2103/agent-company-policy
•	Latest Tag: latest
•	Base Image: python:3.10-slim
Docker Capabilities
•	FastAPI application packaged with all dependencies
•	Environment-variable driven configuration
•	Can be deployed on:
o	Azure App Service (Container)
o	Azure Container Instances
o	AWS ECS / EKS
o	Any Docker-compatible platform
Build & Push Commands
docker build --no-cache -t amitksingh2103/agent-company-policy:latest .
docker push amitksingh2103/agent-company-policy:latest
Local Run Using Docker
docker run -p 8000:8000 --env-file .env amitksingh2103/agent-company-policy:latest
________________________________________
🧠 Design Decisions
•	FAISS chosen for simplicity and fast local retrieval
•	ReAct agent used to clearly demonstrate agent reasoning
•	Session memory implemented for conversational continuity
•	Azure App Service preferred for ease of deployment and evaluation
•	Dockerization completed but code-based deployment used for stability
________________________________________
⚠️ Limitations
•	FAISS runs in-memory (not persistent across restarts)
•	Basic App Service plans may experience cold starts
•	Document domain (can be expanded easily)
•	No authentication layer (intentionally kept simple)
________________________________________
🚀 Future Improvements
•	Replace FAISS with Azure AI Search
•	Add authentication & rate limiting
•	Persist vector store using Azure Blob / Disk
•	Add Azure Monitor & logging
•	Multi-agent orchestration (planner + executor)
•	UI frontend (Streamlit / React)
________________________________________
👤 Author
Amit Kumar Singh
AI Engineer | Generative AI | RAG | LangChain | Azure

