from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_classic.memory import ConversationBufferMemory
from typing import List, Optional
from dotenv import load_dotenv
from langchain_classic import hub
import os

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

llm = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

loader = PyPDFDirectoryLoader("data/")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splitted = splitter.split_documents(docs)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

store = FAISS.from_documents(splitted, embedding=embeddings)
retriever = store.as_retriever(search_kwargs={"k": 5})

prompt = hub.pull("hwchase17/react")

policy_retriever_last_sources = []

@tool
def policy_retriever(query: str):
    """Retrieve relevant policy information from internal company documents."""
    docs = retriever.invoke(query)
    context = []
    sources = set()
    for d in docs:
        context.append(d.page_content)
        sources.add(d.metadata.get("source", "unknown"))
    global policy_retriever_last_sources
    policy_retriever_last_sources = list(sources)
    return "\n".join(context)

agent = create_react_agent(
    llm=llm,
    tools=[policy_retriever],
    prompt=prompt
)

session_memory = {}

def get_memory(session_id):
    if session_id not in session_memory:
        session_memory[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return session_memory[session_id]

app = FastAPI()

class AskRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    source: List[str]

@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    memory = get_memory(payload.session_id or "default")
    executor = AgentExecutor(
    agent=agent,
    tools=[policy_retriever],
    memory=memory,
    return_intermediate_steps=True,
    verbose=True,
    handle_parsing_errors=True)

    result = executor.invoke({
    "input": payload.query
    })
    return {
        "answer": result["output"],
        "source": list(set(policy_retriever_last_sources))
    }
