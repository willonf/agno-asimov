import os
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.skills import LocalSkills, Skills
from agno.tools.file import FileTools
from agno.tools.websearch import WebSearchTools
from dotenv import load_dotenv

load_dotenv()

output_dir = Path(__file__).parent.parent / "output/v1"


file_tools = FileTools(
    base_dir=output_dir,  # diretório onde os arquivos serão salvos
    enable_save_file=True,  # permite salvar arquivos
    enable_read_file=True,  # permite ler arquivos existentes
    enable_list_files=True,  # permite listar arquivos no diretório
)

skills_dir = Path(__file__).parent / "skills"
skills = Skills(loaders=[LocalSkills(str(skills_dir))])


# ─────────────────────────────────────────────────────────────────────────────
# 3. SKILLS (HABILIDADES) — DEFINIDAS VIA PROMPT
#    Skills são instruções detalhadas que ensinam o agente a executar tarefas
#    específicas. São injetadas no prompt do agente como texto.
#
#    Neste projeto, definimos 4 skills que formam o pipeline jornalístico:
#
#    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
#    │  PESQUISA    │ →  │  APURAÇÃO    │ →  │ VERIFICAÇÃO  │ →  │   REDAÇÃO    │
#    │ de Notícias  │    │  de Fontes   │    │   Factual    │    │  da Matéria  │
#    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
#
#    Cada skill define:
#      • Entrada esperada  — o que recebe
#      • Processo          — passos a seguir
#      • Formato de saída  — como deve entregar o resultado
#      • Regras            — restrições a obedecer
# ─────────────────────────────────────────────────────────────────────────────
agent_noticia = Agent(
    name="AGENTE DE NOTICIAS",
    model=OpenAIResponses(id="gpt-5.1-2025-11-13", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[WebSearchTools(), file_tools],
    skills=skills,
    add_datetime_to_context=True,
    markdown=True,
    instructions=[
        "Você é um jornalista completo: pesquisador, apurador, verificador factual e redator.",
        "Receba um tema e execute TODAS as etapas abaixo em sequência.",
        "",
        "Antes de começar, carregue as instruções de cada skill usando get_skill_instructions.",
        "",
        "ETAPA 1 — PESQUISA: use a skill 'pesquisa-noticias'",
        "ETAPA 2 — APURAÇÃO: use a skill 'apuracao-fontes'",
        "ETAPA 3 — VERIFICAÇÃO: use a skill 'verificacao-factual'",
        "ETAPA 4 — REDAÇÃO: use a skill 'redacao-jornalistica'",
        "",
        "Apresente ao usuário APENAS a matéria jornalística final (Etapa 4).",
        "As etapas 1, 2 e 3 são seu processo interno de trabalho.",
        "Salve o documento final em um arquivo .md no diretório",
    ],
)

if __name__ == "__main__":
    agent_noticia.print_response(
        "Modelos avançados de IA realizam hacking de empresas",
        stream=True,
    )
