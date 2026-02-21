# Financial News Agent Pipeline (Prototype)

Lekki prototyp potoku agentów, który:
1. Pobiera listę newsów z Axesso → Yahoo Finance według regionu.
2. Wybiera te najbardziej "interesujące" (na razie: wszystkie). 
3. Pobiera szczegóły dla wybranych artykułów.
4. Redaguje krótkie podsumowania dla ostatnich 24h / 72h / tygodnia / miesiąca.

## Uruchamianie

1. Zainstaluj zależności:

```bash
cd news_agents
python -m pip install -r requirements.txt
```

2. Ustaw zmienne środowiskowe (gdy już będzie klucz Axesso):

- `AXESSO_API_KEY` – klucz autoryzacyjny
- `AXESSO_BASE_URL`, `AXESSO_SEARCH_PATH`, `AXESSO_DETAILS_PATH` (domyślnie `/news/search` i `/news/details`).

3. Uruchom:

```bash
python main.py
```

Jeśli klucza nie ma, skrypt użyje danych mockowych i nadal pozwoli przetestować pipeline.

## Co trzeba dopracować

- [ ] Zebrać dokumentację Axesso (formaty request/response). Zaznaczyłem `TODO` w kodzie (np. `AxessoClient.mock_*`).
- [ ] Redukcja payloadów (agregacja) – teraz nie ma limitu czasu ani cache.
- [ ] UI: można przepiąć `main.py` na Flask / Streamlit / desktopowe GUI gdy zjawi się potrzeba.

## Architektur

- `clients/axesso.py` – zahardcodowane wywołania, sanitizacja (TODO w `sanitize_payload`).
- `agents/preference.py` – użytkownik wybiera region (kontynent) i wysyłany jest request.
- `agents/detail.py` – request po szczegóły.
- `agents/summary.py` – redaguje wiadomość w formie listy.
- `tools/payload_utils.py` – ogranicza pola w requestach/response.

Na teraz output końcowy to zwykły tekst; zapisać można do `news_summary.json`.
