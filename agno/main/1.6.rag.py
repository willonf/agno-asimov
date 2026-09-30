import os
from pathlib import Path

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="agno.db")

knowledge_files = Path(__file__).resolve().parent.parent

# ===== RAG =====

# Initialize ChromaDB
vector_db = ChromaDb(
    collection="empresas_relatorios",
    path="tmp/chromadb",
    embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=os.environ.get("OPENAI_API_KEY")),
    persistent_client=True
)

# Create knowledge base
knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.add_content(
    path=f"{knowledge_files}/docs/PETR",
    reader=PDFReader(chunk_strategy=SemanticChunking()),
    metadata={"company": "Petrobras", "sector": "Petróleo e Gás", "country": "Brazil"},
    skip_if_exists=True  # Evita que o embedding e chunking seja feito sempre que o agente executar
)

knowledge.add_content(
    path=f"{knowledge_files}/docs/VALE",
    reader=PDFReader(chunk_strategy=SemanticChunking()),
    metadata={"company": "Vale", "sector": "Mineração", "country": "Brazil"},
    skip_if_exists=True
)

# AGENT
agent = Agent(
    user_id="user_1",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[YFinanceTools()],
    instructions="Você é um analista e tem diferentes clientes. Lembre-se de cada cliente e suas preferências.",
    add_history_to_context=True,  # Habilita o agente a adicionar informações do histórico no contexto
    db=db,
    num_history_runs=3,
    enable_user_memories=True,  # Armazena memórias do usuário
    enable_agentic_memory=True,
    knowledge=knowledge,  # Adição do conhecimento resultante do RAG
    add_knowledge_to_context=True,
)

if __name__ == "__main__":
    agent.print_response("Olá! Qual foi o lucro líquido da Petrobras em 2T25?", session_id="petrobras_session_4", user_id="analista_petrobras")
    agent.print_response("Olá! O que foi comentado sobre o CAPEX da Vale no 2T25?", session_id="petrobras_session_4", user_id="analista_vale")
