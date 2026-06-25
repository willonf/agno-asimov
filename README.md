# agno-asimov

Projeto de estudos com [Agno](https://github.com/agno-agi/agno), focado em:
- criação de agentes com tools;
- uso de storage para histórico/memória;
- execução de múltiplos agentes via `AgentOS`.

## Visão geral

O app principal está em `main/agent_os.py` e sobe um `AgentOS` com dois agentes:

- **Web Agent**: usa `DuckDuckGoTools` e instrução para sempre incluir fontes.
- **Finance Agent**: usa `YFinanceTools` e instrução para sempre exibir dados em tabela.

Os dois agentes compartilham SQLite em `tmp/agents.db` via `SqliteDb`, com:
- contexto de data/hora;
- histórico das últimas execuções no contexto (`num_history_runs=5`);
- saída em markdown.

## Pré-requisitos

- Python `>= 3.12`
- `uv` (recomendado) ou `pip`

## Instalação

### Opção 1 (recomendada): uv

```bash
uv sync
```

### Opção 2: pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuração de ambiente

Crie um arquivo `.env` na raiz do projeto.

### Variáveis principais

- `OPENAI_API_KEY`: necessária para `main/agent_os.py` (modelo `OpenAIChat`).

### Variáveis usadas nos scripts de exemplo

- `GROQ_API_KEY`: usada nos scripts com `Groq`.
- `TAVILY_API_KEY`: necessária para scripts que usam `TavilyTools`.

## Como executar

### App principal (AgentOS)

```bash
python main/agent_os.py
```

Esse comando sobe o app FastAPI gerado por `AgentOS` com os agentes Web e Finance.

## Scripts de exemplo

Os arquivos em `main/` funcionam como laboratório para recursos específicos:

- `main/0.llm_call.py`: chamada direta de modelo (`Groq`) sem agente.
- `main/1.1.researcher.py`: agente pesquisador com `TavilyTools`.
- `main/1.2.analista-financeiro.py`: agente financeiro com `YFinanceTools`.
- `main/1.3.own-tools.py`: uso de ferramenta customizada Python (`celsius_to_fahrenheit`) junto com `TavilyTools`.
- `main/1.4.storage.py`: demonstra histórico em storage SQLite (`agno.db`) com múltiplas perguntas sequenciais.
- `main/agent_os.py`: composição de múltiplos agentes em um único app.

Exemplo de execução de script:

```bash
python main/1.4.storage.py
```

## Storage e histórico

No Agno, cada conversa é uma sessão. Sem storage, o contexto de execução pode se perder entre runs.

Quando você configura `SqliteDb` no agente (`db=SqliteDb(...)`) e ativa histórico no contexto (`add_history_to_context=True`), o agente passa a recuperar memória recente da sessão para respostas seguintes.

## Dependências principais

Definidas em `pyproject.toml`, incluindo:
- `agno`
- `openai`
- `groq`
- `fastapi` e `uvicorn`
- `sqlalchemy`
- `ddgs`, `tavily-python`, `yfinance`

## Estrutura rápida

```text
.
├── main/
│   ├── 0.llm_call.py
│   ├── 1.1.researcher.py
│   ├── 1.2.analista-financeiro.py
│   ├── 1.3.own-tools.py
│   ├── 1.4.storage.py
│   └── agent_os.py
├── notes.md
├── pyproject.toml
└── README.md
```
