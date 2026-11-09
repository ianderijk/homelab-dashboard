# dashboard

Web frontend for the homelab dashboard. A small FastAPI app renders Jinja2
templates server-side and uses [htmx](https://htmx.org) to refresh the overview
panel on an interval. All data comes from the homelab API over HTTP; the
dashboard never reads the SQLite database directly.

## Running

```bash
make api          # the dashboard needs the API running
make dashboard    # serves on http://127.0.0.1:8001
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DASHBOARD_API_URL` | `http://127.0.0.1:8000` | Base URL of the homelab API |
| `DASHBOARD_HOST` | `127.0.0.1` | Interface to bind |
| `DASHBOARD_PORT` | `8001` | Port to bind |
| `DASHBOARD_REFRESH_SECONDS` | `60` | How often the overview panel refreshes |
| `DASHBOARD_API_TIMEOUT_SECONDS` | `5` | Per-request timeout when calling the API |

## Layout

| Path | Role |
|---|---|
| `client.py` | One method per API endpoint. Connection failures raise `ApiUnavailableError`; a 404 for a single service or disc returns `None` (no data recorded yet). |
| `overview.py` | Fetches everything shown on the page in one pass, so the summary tiles and the detail panels always agree. |
| `app.py` | Routes: `/` renders the full page, `/panels/overview` renders the fragment htmx swaps in on each refresh. |
| `templates/` | `index.html` is the page shell; `partials/` holds the overview fragment and its panels. |
| `static/` | `style.css` and a vendored `htmx.min.js` (2.0.11, verified against the npm registry integrity hash). |

## Visual conventions

- Colours follow the reference data-viz palette, with light and dark variants
  chosen from the OS setting.
- Status is never shown by colour alone: every up/down/low badge carries an
  icon and a text label.
- A disc meter turns red, with a "Low space" badge, when its free fraction drops
  below the API's `warning` threshold. The tick on the meter marks that threshold.
- The Pi CPU temperature tile (from `/latest-temp`) is green below the API's
  `warning` value, amber from `warning` up to and including `critical`, and red
  above `critical`. The colour sits on the badge and the tile's top edge; the
  number itself stays in the normal text colour so it remains legible.
- While a refresh is in flight, the panel dims instead of being cleared, so the
  layout never jumps.

## Checks

```bash
make check    # ruff, ty, djlint (templates), biome (CSS)
make test
```
