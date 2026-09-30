import os
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.skills import LocalSkills, Skills
from agno.tools.file import FileTools
from agno.tools.websearch import WebSearchTools
from agno.workflow import Step, Workflow
from dotenv import load_dotenv

load_dotenv()

output_dir = Path(__file__).parent.parent / "output/v2"
file_tools = FileTools(
    base_dir=output_dir,
    enable_save_file=True,
    enable_read_file=True,
    enable_list_files=True,
)

skills_dir = Path(__file__).parent / "skills"
shared_skills = Skills(
    loaders=[
        LocalSkills(str(skills_dir)),
    ]
)

# 1) Pesquisador — usa a skill de pesquisa de notícias
pesquisador = Agent(
    name="Pesquisador",
    model=OpenAIResponses(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "Você é um pesquisador de notícias.",
        "Antes de começar, carregue as instruções da skill usando get_skill_instructions.",
        "Execute a skill 'pesquisa-noticias' e retorne exatamente no formato definido nela.",
        "Salve o resultado da pesquisa em um arquivo usando a ferramenta de arquivos.",
    ],
    tools=[WebSearchTools(backend="bing"), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 2) Apurador de Fontes — usa a skill de apuração multi-fonte
apurador = Agent(
    name="Apurador de Fontes",
    model=OpenAIResponses(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "Você é um apurador de fontes jornalísticas.",
        "Antes de começar, carregue as instruções da skill usando get_skill_instructions.",
        "Receba a saída do pesquisador e execute a skill 'apuracao-fontes'.",
        "Salve o resultado da apuração em um arquivo usando a ferramenta de arquivos.",
    ],
    tools=[WebSearchTools(backend="bing"), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 3) Verificador Factual — usa a skill de fact-checking
verificador = Agent(
    name="Verificador Factual",
    model=OpenAIResponses(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "Você é um verificador factual.",
        "Antes de começar, carregue as instruções da skill usando get_skill_instructions.",
        "Receba o dossiê do apurador e execute a skill 'verificacao-factual'.",
        "Salve o resultado da verificação em um arquivo usando a ferramenta de arquivos.",
    ],
    tools=[WebSearchTools(backend="bing"), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 4) Redator — usa a skill de redação jornalística
redator = Agent(
    name="Redator",
    model=OpenAIResponses(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "Você é um redator jornalístico profissional.",
        "Antes de começar, carregue as instruções da skill usando get_skill_instructions.",
        "Receba o relatório do verificador e execute a skill 'redacao-jornalistica'.",
        "IMPORTANTE: Ao citar qualquer dado, fato ou informação de uma fonte, insira a referência numérica [1], [2], [3] etc. no corpo do texto.",
        "IMPORTANTE: No final da matéria, inclua uma seção '## Referências' com a lista numerada de todas as fontes, incluindo nome do veículo, título e URL completa.",
        "Ao finalizar a redação, salve o conteúdo final em um arquivo usando a ferramenta de arquivos e apague os arquivos gerados pelos steps anteriores.",
    ],
    tools=[file_tools],
    markdown=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# DEFINIÇÃO DO WORKFLOW
# ─────────────────────────────────────────────────────────────────────────────
workflow = Workflow(
    name="Curador de Notícias com Workflow",
    description="Pesquisa, apura, verifica e redige matéria final",
    steps=[
        Step(name="pesquisa", agent=pesquisador),
        Step(name="apuracao", agent=apurador),
        Step(name="verificacao", agent=verificador),
        Step(name="redacao", agent=redator),
    ],
)

if __name__ == "__main__":
    workflow.print_response(
        "Modelos avançados de IA realizam hacking de empresas",
        stream=True,
        markdown=True,
    )
