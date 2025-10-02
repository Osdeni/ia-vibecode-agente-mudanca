from __future__ import annotations

from collections import namedtuple
from csv import DictReader
from pathlib import Path
from typing import List


CityProfile = namedtuple(
    "CityProfile",
    [
        "city",
        "state",
        "distance_km_from_home",
        "region_type",
        "climate_summary",
        "climate_dry_or_humid",
        "climate_hot_or_cold",
        "summer_avg_c",
        "winter_avg_c",
        "rain_days_year",
        "crime_index",
        "quality_of_life_index",
        "internet_avg_mbps",
        "notes",
        "sources",
        "collected_at",
    ],
)


def load_cities() -> List[CityProfile]:
    data_path = Path("data") / "cidades.csv"
    cities: List[CityProfile] = []
    with data_path.open(newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            cities.append(
                CityProfile(
                    row.get("city", ""),
                    row.get("state", ""),
                    row.get("distance_km_from_home", ""),
                    row.get("region_type", ""),
                    row.get("climate_summary", ""),
                    row.get("climate_dry_or_humid", ""),
                    row.get("climate_hot_or_cold", ""),
                    row.get("summer_avg_c", ""),
                    row.get("winter_avg_c", ""),
                    row.get("rain_days_year", ""),
                    row.get("crime_index", ""),
                    row.get("quality_of_life_index", ""),
                    row.get("internet_avg_mbps", ""),
                    row.get("notes", ""),
                    row.get("sources", ""),
                    row.get("collected_at", ""),
                )
            )
    return cities


def score_city(profile: CityProfile, weights: dict) -> float:
    return 0.0


def print_city_profiles() -> None:
    for profile in load_cities():
        print(profile)


def main() -> None:
    cities = load_cities()
    print(len(cities))
    for profile in cities:
        print(profile.city)


if __name__ == "__main__":
    main()
