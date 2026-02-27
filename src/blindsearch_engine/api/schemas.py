from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    territory_id: int = Field(..., ge=1)
    combination_id: int = Field(..., ge=1)
    strategy: Literal["bfs_limited", "dfs_limited"] = "bfs_limited"
    depth_limit: int = Field(6, ge=1, le=50)
    max_trace_steps: int = Field(1200, ge=1, le=10000)
    max_states: int = Field(50000, ge=100, le=1000000)
    early_stop: bool = True


class CompareRequest(BaseModel):
    territory_id: int = Field(..., ge=1)
    combination_id: int = Field(..., ge=1)
    depth_limit: int = Field(6, ge=1, le=50)
    max_states: int = Field(50000, ge=100, le=1000000)
