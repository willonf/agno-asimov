import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.vectordb.chroma import ChromaDb
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

vector_db = ChromaDb(
    collection="pdf_agent",
    path="tmp/chromadb",
    persistent_client=True,
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)

knowledge = Knowledge(vector_db=vector_db)
db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
    id="agent_pdf",
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    knowledge=knowledge,
    add_history_to_context=True,
    search_knowledge=True,
    debug_mode=True,
)

agent_os = AgentOS(name="agente_pdf", agents=[agent])

app = agent_os.get_app()

if __name__ == "__main__":
    # knowledge.insert(
    #     url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",
    #     metadata={
    #         "source": "Grendene",
    #         "type": "pdf",
    #         "description": "Relatório Trimestral 2T25",
    #     },
    #     skip_if_exists=True,
    #     reader=PDFReader(),
    # )
    agent_os.serve(app="ex2:app", reload=True)
