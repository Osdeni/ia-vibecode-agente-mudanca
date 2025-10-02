"""Exemplo simples de uso do LangChain com a tool de cidades."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

from langchain_city_tool import listar_perfis_cidades


def main() -> None:
    """Executa um agente LangChain utilizando o modelo da OpenAI."""
    load_dotenv(dotenv_path=Path.cwd() / ".env")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError(
            "Defina a variável OPENAI_API_KEY em um arquivo .env ou no ambiente."
        )
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
    )
    resposta = agent.run("Quais cidades estão disponíveis?")
    print("\nResposta do agente:\n", resposta)


if __name__ == "__main__":
    main()
