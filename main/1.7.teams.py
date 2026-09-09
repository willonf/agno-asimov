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

from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

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

# AGENTS
agent = Agent(
    user_id="user_1",
    model=Groq(id="llama-3.3-70b-versatile"),
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


analista_noticias_agent = Agent(
    name="analista_noticias",
    model=Groq(id="llama-3.3-70b-versatile"),
    role="Você é um pesquisador de noticias",
    instructions=[
        "Use suas tools de busca para encontrar informações na web sobre empresas listadas na B3."
    ],
    tools=[DuckDuckGoTools(enable_search=False, enable_news=True)],
    markdown=True,
)

analista_cotacoes_agent = Agent(
    name="analista_cotacoes",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Você é um analista de cotações de empresas listadas na B3."
    ],
    tools=[YFinanceTools()],
    markdown=True,
)


analista_team = Team (
    name="analista_team",
    model=Groq(id="llama-3.3-70b-versatile"),
    members=[analista_noticias_agent, analista_cotacoes_agent],
    instructions=[
        "Você deve entender as informações solicitadas pelo usuário e fornecer uma resposta adequada",
        "Para obter informações sobre balanço e DRE, utilize o analista_relatorio",
        "Para obter informações sobre cotações, utilize o analista_cotacoes",
        "Para obter informações sobre notícias, utilize o analista_noticias"
    ],
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    show_members_responses=True,
    get_member_information_tool=True,
    add_datetime_to_context=True,
    markdown=True,
    debug_mode=True,
)

if __name__ == "__main__":
    analista_team.print_response("Olá! Qual foi o lucro líquido da petrobras em 2T25 segundo o relatório publicado?", session_id="petrobras_session_9", user_id="analista_petro")
