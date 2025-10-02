"""Exemplo simples de uso do LangChain com as tools de cidades."""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain_openai import ChatOpenAI

from city_profiles import load_cities
from langchain_city_tool import listar_perfis_cidades
from route_analysis_tool import (
    RouteAnalysis,
    analisar_rota_cidades,
    build_route_analysis_chain,
)


def _configure_langsmith_tracer() -> LangChainTracer | None:
    """Cria um tracer configurado para o LangSmith, caso o tracing esteja ativo."""

    tracing_env = os.getenv("LANGSMITH_TRACING", "").strip().lower()
    tracing_enabled = tracing_env in {"1", "true", "yes", "on"}
    if not tracing_enabled:
        return None

    project_name = os.getenv("LANGSMITH_PROJECT") or "default"
    tracer = LangChainTracer(project_name=project_name)
    tracer.load_default_session()
    print(
        "LangSmith tracing habilitado.",
        f"Projeto: {project_name}",
        f"Endpoint: {os.getenv('LANGSMITH_ENDPOINT', 'padrão')}",
        sep="\n",
    )
    return tracer


def main() -> None:
    """Executa um agente LangChain utilizando o modelo da OpenAI."""
    load_dotenv(dotenv_path=Path.cwd() / ".env")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError(
            "Defina a variável OPENAI_API_KEY em um arquivo .env ou no ambiente."
        )

    tracer = _configure_langsmith_tracer()
    callbacks = [tracer] if tracer else []
    callback_manager = CallbackManager(callbacks) if callbacks else None

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai_api_key,
    )
    agent = initialize_agent(
        tools=[listar_perfis_cidades],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        callback_manager=callback_manager,
    )
    invoke_config = {"callbacks": callbacks} if callbacks else None

    resposta = agent.invoke(
        "Quais cidades estão disponíveis?",
        config=invoke_config,
    )
    print("\nResposta do agente:\n", resposta)

    print("\nAnálises detalhadas das rotas a partir de Criciúma:\n")
    origem = "Criciúma"
    destinos = []
    entradas = []
    for profile in load_cities():
        destino = f"{profile.city}, {profile.state}".strip().strip(",")
        if not destino or profile.city.lower() == origem.lower():
            continue

        destinos.append(destino)
        entradas.append({"origem": origem, "destino": destino})

    analises: list[RouteAnalysis] = build_route_analysis_chain().map().invoke(
        entradas,
        config=invoke_config,
    )

    for destino, analise in zip(destinos, analises):
        print(f"Rota: {origem} -> {destino}")
        print(json.dumps(analise.dict(), ensure_ascii=False, indent=2))
        print("-" * 40)


if __name__ == "__main__":
    main()
