"""Tool que gera um resumo de rota entre duas cidades utilizando um LLM."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI


class RainData(BaseModel):
    """Informações de chuva para um determinado ano."""

    year: int = Field(..., description="Ano da medição de dias chuvosos.")
    days: int = Field(..., description="Quantidade de dias chuvosos no ano informado.")


class RouteAnalysis(BaseModel):
    """Estrutura do JSON retornado pelo modelo para a análise de rota."""

    distance_km_from_home: float = Field(
        ..., description="Distância aproximada entre origem e destino em quilômetros."
    )
    region_type: str = Field(
        ..., description="Descrição sucinta do tipo de região do destino (praia, serra etc.)."
    )
    climate_summary: List[str] = Field(
        ...,
        description="Três tópicos curtos resumindo o clima típico do destino.",
        min_items=3,
        max_items=3,
    )
    rain_days_year: RainData = Field(
        ..., description="Registro de dias chuvosos com o ano utilizado como referência."
    )


class _RouteAnalysisInput(BaseModel):
    origem: str = Field(..., description="Cidade de origem.")
    destino: str = Field(..., description="Cidade de destino.")


@lru_cache(maxsize=1)
def _build_parser() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=RouteAnalysis)


_LLM: ChatOpenAI | None = None


def _get_llm() -> ChatOpenAI:
    """Retorna uma instância reutilizável do modelo de chat da OpenAI."""
    global _LLM
    if _LLM is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise RuntimeError(
                "Defina a variável OPENAI_API_KEY no ambiente antes de usar a tool."
            )
        _LLM = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_api_key,
        )
    return _LLM


@lru_cache(maxsize=1)
def _build_prompt() -> ChatPromptTemplate:
    parser = _build_parser()
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Você é um especialista em viagens brasileiras. Forneça apenas o JSON"
                " solicitado e siga rigorosamente estas instruções de formato:\n"
                "{format_instructions}",
            ),
            (
                "human",
                "Considere as fontes públicas mais confiáveis. Para a cidade de origem"
                " '{origem}' e a cidade de destino '{destino}', produza o JSON com"
                " distância, tipo de região, resumo climático em três tópicos e dias"
                " chuvosos no ano mais recente disponível.",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())


@lru_cache(maxsize=1)
def _build_chain():
    parser = _build_parser()
    prompt = _build_prompt()
    llm = _get_llm()
    return prompt | llm | parser


def _gerar_resumo_rota(origem: str, destino: str) -> str:
    """Gera o resumo da rota em formato JSON usando o modelo da OpenAI."""
    chain = _build_chain()
    resultado: RouteAnalysis = chain.invoke({"origem": origem, "destino": destino})
    return resultado.json(ensure_ascii=False)


def build_route_analysis_chain():
    """Retorna o encadeamento LCEL utilizado pela tool de análise de rotas."""
    return _build_chain()


analisar_rota_cidades = StructuredTool.from_function(
    func=_gerar_resumo_rota,
    name="analisar_rota_cidades",
    description=(
        "Recebe uma cidade de origem e outra de destino e retorna um JSON com "
        "distância estimada, tipo de região, resumo climático (três tópicos) e uma "
        "estimativa de dias chuvosos no ano mais recente informado."
    ),
    args_schema=_RouteAnalysisInput,
)


__all__ = [
    "analisar_rota_cidades",
    "RouteAnalysis",
    "RainData",
    "build_route_analysis_chain",
]
