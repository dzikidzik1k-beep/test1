"""Entry point for the prototype news-agent pipeline."""
from __future__ import annotations

import json
import sys

from rich import print as rprint

from news_agents.agents.detail import DetailAgent
from news_agents.agents.preference import PreferenceAgent
from news_agents.agents.summary import SummaryAgent
from news_agents.clients.axesso import AxessoClient
from news_agents.config import AXESSO_CONFIG


def main() -> int:
    client = AxessoClient(AXESSO_CONFIG)
    pref_agent = PreferenceAgent(client)
    detail_agent = DetailAgent(client)
    summary_agent = SummaryAgent()

    rprint("[bold green]Pipeline start: wybieranie newsów[/bold green]")
    try:
        region = pref_agent.prompt_region()
    except ValueError as err:
        rprint(f"[red]Błąd:[/red] {err}")
        return 1

    query = input("Podaj słowa kluczowe (opcjonalnie): ").strip() or None
    max_items = input("Maksymalna liczba artykułów do pobrania (domyślnie 10): ").strip()
    limit = int(max_items) if max_items.isdigit() else 10

    news = pref_agent.pick_interesting_news(region, query=query, limit=limit)
    if not news:
        rprint("[yellow]Brak wyników. Sprawdź inne preferencje lub poczekaj chwilę.[/yellow]")
        return 0

    rprint(f"Wybrano {len(news)} newsów. Wysyłam po szczegóły...\n")
    detail_ids = [item["id"] for item in news if item.get("id")]
    detailed = detail_agent.fetch(detail_ids)

    summaries = summary_agent.summarize(detailed)
    rprint("[bold blue]Redakcje:[/bold blue]")
    for bucket, items in summaries.items():
        rprint(f"\n[cyan]{bucket.replace('_', ' ')} ({len(items)}):[/cyan]")
        for entry in items:
            rprint(f"- {entry}")

    rprint("\nGotowe. Możesz przekazać redakcję dalej lub zapisać ją do pliku.")
    save = input("Zapisz do pliku JSON? (t/n): ").strip().lower()
    if save == "t":
        output = {
            "region": region,
            "query": query,
            "summaries": summaries,
        }
        path = "news_summary.json"
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(output, fp, ensure_ascii=False, indent=2)
        rprint(f"Zapisano do {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
