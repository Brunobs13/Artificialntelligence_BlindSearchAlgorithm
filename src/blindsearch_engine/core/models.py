from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

Position = Tuple[int, int]
State = Tuple[Position, ...]


@dataclass(frozen=True)
class StationCombination:
    id: int
    stations: Tuple[Position, ...]
    radii: Tuple[int, ...]


@dataclass(frozen=True)
class TerritoryProblem:
    id: int
    name: str
    matrix: Tuple[Tuple[int, ...], ...]
    budget: int
    targets: Tuple[int, ...]
    corporate_context: str


@dataclass(frozen=True)
class SearchRunConfig:
    strategy: str
    depth_limit: int
    max_trace_steps: int = 1500
    max_states: int = 100000
    early_stop: bool = True


@dataclass(frozen=True)
class TargetHit:
    target: int
    step_index: int
    depth: int
    coverage: int
    generated_states: int


@dataclass(frozen=True)
class SearchStep:
    index: int
    depth: int
    positions: Tuple[Position, ...]
    protected_families: int
    generated_states: int
    expansions: int
    frontier_size: int
    reached_targets: Tuple[int, ...]


def to_tuple_matrix(matrix: Sequence[Sequence[int]]) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(row) for row in matrix)


def to_tuple_positions(positions: Sequence[Sequence[int]]) -> Tuple[Position, ...]:
    return tuple((int(x), int(y)) for x, y in positions)


def to_tuple_int(values: Sequence[int]) -> Tuple[int, ...]:
    return tuple(int(value) for value in values)


def serialize_step(step: SearchStep) -> dict:
    return {
        "index": step.index,
        "depth": step.depth,
        "positions": [list(position) for position in step.positions],
        "protectedFamilies": step.protected_families,
        "generatedStates": step.generated_states,
        "expansions": step.expansions,
        "frontierSize": step.frontier_size,
        "reachedTargets": list(step.reached_targets),
    }


def serialize_hits(hits: List[TargetHit]) -> List[dict]:
    return [
        {
            "target": hit.target,
            "stepIndex": hit.step_index,
            "depth": hit.depth,
            "coverage": hit.coverage,
            "generatedStates": hit.generated_states,
        }
        for hit in hits
    ]
