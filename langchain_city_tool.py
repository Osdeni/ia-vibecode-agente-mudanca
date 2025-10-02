"""LangChain tool for accessing city profile data."""
from __future__ import annotations

from typing import Iterable

from langchain.tools import tool

from city_profiles import CityProfile, load_cities


def _format_city(profile: CityProfile) -> str:
    """Convert a :class:`CityProfile` into a readable summary string."""
    return (
        f"{profile.city}, {profile.state} | "
        f"Distância: {profile.distance_km_from_home} km | "
        f"Clima: {profile.climate_summary} | "
        f"Notas: {profile.notes}"
    )


def _summarise_cities(cities: Iterable[CityProfile]) -> str:
    lines = ["Perfis de cidades disponíveis:"]
    for profile in cities:
        lines.append(_format_city(profile))
    return "\n".join(lines)


@tool("listar_perfis_cidades")
def listar_perfis_cidades(_: str = "") -> str:
    """Retorna um resumo dos perfis de cidades disponíveis no dataset."""
    cities = load_cities()
    if not cities:
        return "Nenhum perfil de cidade encontrado."
    return _summarise_cities(cities)


__all__ = ["listar_perfis_cidades"]
