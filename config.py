"""Configuration helpers shared across the news pipeline."""
from dataclasses import dataclass
from typing import Dict
import os


@dataclass(frozen=True)
class AxessoConfig:
    base_url: str
    search_path: str
    details_path: str
    api_key: str


AXESSO_CONFIG = AxessoConfig(
    base_url=os.getenv("AXESSO_BASE_URL", "https://api.axesso.com/v1"),
    search_path=os.getenv("AXESSO_SEARCH_PATH", "/news/search"),
    details_path=os.getenv("AXESSO_DETAILS_PATH", "/news/details"),
    api_key=os.getenv("AXESSO_API_KEY", ""),  # TODO: put the real key via env
)

REGION_TO_FILTER: Dict[str, Dict[str, str]] = {
    "africa": {"continent": "Africa"},
    "asia": {"continent": "Asia"},
    "europe": {"continent": "Europe"},
    "north_america": {"continent": "North America"},
    "south_america": {"continent": "South America"},
    "oceania": {"continent": "Oceania"},
}

DEFAULT_REGION = "europe"
