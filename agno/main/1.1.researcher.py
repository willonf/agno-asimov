from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools()],
    debug_mode=True
)

if __name__ == "__main__":
    agent.print_response("Use suas ferramentas para pesquisar a temperatura de hoje em Manaus")



