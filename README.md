# Company Policy Q&A System (RAG-based)

This project implements a **Retrieval-Augmented Generation (RAG)** based question-answering system over internal company policy documents using **LangChain, Azure OpenAI, FAISS, and FastAPI**.

The system allows users to query company policies and receive accurate, source-grounded answers.

---

## 🔧 Tech Stack

- **Python 3.10**
- **FastAPI** – REST API
- **LangChain (Classic + Community)**
- **Azure OpenAI (GPT-4o-mini + text-embedding-3-large)**
- **FAISS (CPU)** – Vector database
- **Docker** – Containerization
- **Azure App Service** – Deployment

---

## 🧠 Architecture Overview

1. Company policy PDFs are loaded and split into chunks
2. Chunks are embedded using Azure OpenAI Embeddings
3. FAISS is used for semantic similarity search
4. A ReAct-based LangChain agent retrieves relevant policy context
5. The LLM generates answers strictly grounded in retrieved documents
6. Responses include both **answers and source references**

---

## 📂 Data Source

- `Company_Policy_Handbook.pdf`
  - Code of Conduct
  - Leave Policy
  - Remote Work Policy
  - Data Protection & Information Security Policy

---

## 🚀 API Endpoint

### POST `/ask`

**Request Body**
```json
{
  "query": "What are the different policies of the company?",
  "session_id": "user123"
}
Response

json
Copy code
{
  "answer": "The company policies include...",
  "source": ["data/Company_Policy_Handbook.pdf"]
}
🐳 Dockerization
The application was fully containerized using Docker.

Build Image
bash
Copy code
docker build --no-cache -t amitksingh2103/agent-company-policy:latest .
Push to Docker Hub
bash
Copy code
docker push amitksingh2103/agent-company-policy:latest
Docker Hub Repository:
👉 https://hub.docker.com/r/amitksingh2103/agent-company-policy

☁️ Deployment Strategy (Azure)
Final Deployment Choice
Azure App Service (Linux)

Pricing Plan: F1 (Free Tier)

Rationale
While the application was successfully containerized and pushed to Docker Hub, the final deployment was done via direct code deployment on Azure App Service (F1) to:

Avoid unnecessary cloud costs

Ensure faster evaluation access

Match assignment-scale infrastructure needs

This approach demonstrates both containerization expertise and practical cloud decision-making.

⚙️ Environment Variables
Configured securely in Azure App Service:

env
Copy code
AZURE_OPENAI_API_KEY=****
AZURE_OPENAI_ENDPOINT=https://first500days-openai.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
🌐 Live API
Swagger UI:
👉 https://agent-company-policy-api.azurewebsites.net/docs

✅ Assignment Coverage
✔ RAG implementation

✔ Azure OpenAI integration

✔ Vector database (FAISS)

✔ API-based interaction

✔ Dockerized application

✔ Cloud deployment on Azure

✔ Production-style architecture

👤 Author
Amit Kumar Singh
Generative AI Engineer
