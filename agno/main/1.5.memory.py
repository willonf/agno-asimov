from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

load_dotenv()

db = SqliteDb(db_file="agno.db")

# é possivel criar um memory manager, para gerenciar a memória do agente

agent = Agent(
    user_id="user_1",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[YFinanceTools()],
    instructions="Você é um analista e tem diferentes clientes. Lembre-se de cada cliente e suas preferências.",
    add_history_to_context=True,  # Habilita o agente a adicionar informações do histórico no contexto
    db=db,
    num_history_runs=3,
    enable_user_memories=True,  # Armazena memórias do usuário
    enable_agentic_memory=True
)

if __name__ == "__main__":
    # agent.print_response("Qual a cotação atual da Petrobras?", session_id="petrobras_session", user_id="analista_petrobras")
    # agent.print_response("Qual a cotação atual da Vale?", session_id="vale_session", user_id="analista_vale")
    agent.print_response("Já consultei a cotação de quais empresas?", session_id="petrobras_session",
                         user_id="analista_petrobras")
