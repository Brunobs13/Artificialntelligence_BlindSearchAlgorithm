from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ..core.data import get_budget_used, get_combination, get_combinations_for_budget, get_territory, list_territories
from ..core.models import SearchRunConfig
from ..engine.search import compare_strategies, run_search
from ..utils.logging import configure_logging
from ..utils.settings import settings
from .schemas import CompareRequest, RunRequest

configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Corporate Blind Search Control Room",
    version="2.0.0",
    description="Operational dashboard API for depth-limited blind-search simulation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/assets", StaticFiles(directory=str(STATIC_DIR)), name="assets")


def serialize_combination(combination) -> Dict[str, object]:
    return {
        "id": combination.id,
        "stations": [list(station) for station in combination.stations],
        "radii": list(combination.radii),
        "budgetUsed": get_budget_used(combination.radii),
    }


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/api/territories")
def territories() -> Dict[str, List[Dict[str, object]]]:
    items: List[Dict[str, object]] = []
    for territory in list_territories():
        items.append(
            {
                "id": territory.id,
                "name": territory.name,
                "budget": territory.budget,
                "targets": list(territory.targets),
                "rows": len(territory.matrix),
                "cols": len(territory.matrix[0]),
                "corporateContext": territory.corporate_context,
            }
        )
    return {"territories": items}


@app.get("/api/territories/{territory_id}")
def territory_details(territory_id: int) -> Dict[str, object]:
    try:
        territory = get_territory(territory_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    combinations = [serialize_combination(c) for c in get_combinations_for_budget(territory.budget)]
    return {
        "id": territory.id,
        "name": territory.name,
        "budget": territory.budget,
        "targets": list(territory.targets),
        "matrix": [list(row) for row in territory.matrix],
        "corporateContext": territory.corporate_context,
        "combinations": combinations,
    }


@app.get("/api/territories/{territory_id}/combinations")
def territory_combinations(territory_id: int) -> Dict[str, object]:
    try:
        territory = get_territory(territory_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    combinations = [serialize_combination(c) for c in get_combinations_for_budget(territory.budget)]
    return {
        "territoryId": territory.id,
        "budget": territory.budget,
        "combinations": combinations,
    }


@app.post("/api/run")
def run_algorithm(payload: RunRequest) -> Dict[str, object]:
    try:
        territory = get_territory(payload.territory_id)
        combination = get_combination(territory.budget, payload.combination_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    logger.info(
        "running strategy=%s territory=%s combination=%s depth=%s",
        payload.strategy,
        payload.territory_id,
        payload.combination_id,
        payload.depth_limit,
    )

    config = SearchRunConfig(
        strategy=payload.strategy,
        depth_limit=payload.depth_limit,
        max_trace_steps=payload.max_trace_steps,
        max_states=payload.max_states,
        early_stop=payload.early_stop,
    )

    result = run_search(territory, combination, config)
    return result


@app.post("/api/compare")
def compare_algorithms(payload: CompareRequest) -> Dict[str, object]:
    try:
        territory = get_territory(payload.territory_id)
        combination = get_combination(territory.budget, payload.combination_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    logger.info(
        "comparing territory=%s combination=%s depth=%s",
        payload.territory_id,
        payload.combination_id,
        payload.depth_limit,
    )

    return compare_strategies(
        territory=territory,
        combination=combination,
        depth_limit=payload.depth_limit,
        max_states=payload.max_states,
    )
