from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dashboard.client import ApiClient, ApiUnavailableError
from dashboard.config import Settings, load_settings
from dashboard.formatting import celsius, percent, size_from_gib
from dashboard.overview import Overview, fetch_overview

PACKAGE_DIR = Path(__file__).parent

templates = Jinja2Templates(directory=PACKAGE_DIR / "templates")
templates.env.filters["percent"] = percent
templates.env.filters["size"] = size_from_gib
templates.env.filters["celsius"] = celsius


def get_api(request: Request) -> ApiClient:
    return request.app.state.api


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


ApiDep = Annotated[ApiClient, Depends(get_api)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def _try_fetch_overview(api: ApiClient) -> Overview | None:
    try:
        return fetch_overview(api)
    except ApiUnavailableError:
        return None


def _render(
    request: Request, template: str, api: ApiClient, settings: Settings
) -> HTMLResponse:
    overview = _try_fetch_overview(api)
    context = {
        "overview": overview,
        "api_offline": overview is None,
        "refresh_seconds": settings.refresh_seconds,
    }
    return templates.TemplateResponse(request, template, context)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        with httpx.Client(
            base_url=settings.api_url, timeout=settings.api_timeout_seconds
        ) as http:
            app.state.api = ApiClient(http)
            yield

    app = FastAPI(title="Homelab dashboard", lifespan=lifespan)
    app.state.settings = settings
    app.mount("/static", StaticFiles(directory=PACKAGE_DIR / "static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request, api: ApiDep, settings: SettingsDep) -> HTMLResponse:
        return _render(request, "index.html", api, settings)

    @app.get("/panels/overview", response_class=HTMLResponse)
    def overview_panel(
        request: Request, api: ApiDep, settings: SettingsDep
    ) -> HTMLResponse:
        return _render(request, "partials/overview.html", api, settings)

    return app


app = create_app()
