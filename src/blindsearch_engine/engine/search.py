from __future__ import annotations

from collections import deque
from time import perf_counter
from typing import Deque, Dict, Iterable, List, Set, Tuple

from ..core.models import (
    SearchRunConfig,
    SearchStep,
    State,
    StationCombination,
    TargetHit,
    TerritoryProblem,
    serialize_hits,
    serialize_step,
)

MOVES: Tuple[Tuple[int, int], ...] = ((0, -1), (1, 0), (0, 1), (-1, 0))


def within_bounds(x: int, y: int, matrix: Tuple[Tuple[int, ...], ...]) -> bool:
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])


def station_fits(position: Tuple[int, int], radius: int, matrix: Tuple[Tuple[int, ...], ...]) -> bool:
    x, y = position
    return within_bounds(x - radius, y - radius, matrix) and within_bounds(x + radius, y + radius, matrix)


def calculate_coverage(
    state: State,
    radii: Tuple[int, ...],
    matrix: Tuple[Tuple[int, ...], ...],
) -> Tuple[int, Set[Tuple[int, int]]]:
    protected_cells: Set[Tuple[int, int]] = set()
    protected_families = 0

    for (cx, cy), radius in zip(state, radii):
        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                if within_bounds(x, y, matrix) and (x, y) not in protected_cells:
                    protected_cells.add((x, y))
                    protected_families += matrix[x][y]

    return protected_families, protected_cells


def generate_neighbors(
    state: State,
    radii: Tuple[int, ...],
    matrix: Tuple[Tuple[int, ...], ...],
) -> Iterable[State]:
    for station_idx, (x, y) in enumerate(state):
        radius = radii[station_idx]
        for dx, dy in MOVES:
            next_position = (x + dx, y + dy)
            if next_position in state:
                continue
            if not station_fits(next_position, radius, matrix):
                continue

            updated_state = list(state)
            updated_state[station_idx] = next_position
            yield tuple(updated_state)


def run_search(
    territory: TerritoryProblem,
    combination: StationCombination,
    config: SearchRunConfig,
) -> Dict[str, object]:
    start = perf_counter()

    start_state: State = tuple(combination.stations)
    frontier: Deque[Tuple[State, int]] = deque([(start_state, 0)])
    visited: Set[State] = {start_state}

    generated_states = 1
    expansions = 0
    terminated_by_state_cap = False

    start_coverage, _ = calculate_coverage(start_state, combination.radii, territory.matrix)
    best_state = start_state
    best_coverage = start_coverage

    target_hits: Dict[int, TargetHit] = {}
    reached_targets: List[int] = [target for target in territory.targets if start_coverage >= target]
    for target in reached_targets:
        target_hits[target] = TargetHit(target, 0, 0, start_coverage, generated_states)

    trace: List[SearchStep] = [
        SearchStep(
            index=0,
            depth=0,
            positions=start_state,
            protected_families=start_coverage,
            generated_states=generated_states,
            expansions=expansions,
            frontier_size=len(frontier),
            reached_targets=tuple(sorted(reached_targets)),
        )
    ]

    should_stop = config.early_stop and len(target_hits) == len(territory.targets)
    trace_index = 0

    while frontier and not should_stop:
        if config.strategy == "bfs_limited":
            state, depth = frontier.popleft()
        else:
            state, depth = frontier.pop()

        if depth >= config.depth_limit:
            continue

        expansions += 1
        for next_state in generate_neighbors(state, combination.radii, territory.matrix):
            if next_state in visited:
                continue

            visited.add(next_state)
            generated_states += 1
            next_depth = depth + 1
            coverage, _ = calculate_coverage(next_state, combination.radii, territory.matrix)

            if coverage > best_coverage:
                best_coverage = coverage
                best_state = next_state

            hit_targets: List[int] = []
            for target in territory.targets:
                if target in target_hits:
                    continue
                if coverage >= target:
                    target_hits[target] = TargetHit(target, trace_index + 1, next_depth, coverage, generated_states)
                    hit_targets.append(target)

            frontier.append((next_state, next_depth))

            trace_index += 1
            if len(trace) < config.max_trace_steps:
                trace.append(
                    SearchStep(
                        index=trace_index,
                        depth=next_depth,
                        positions=next_state,
                        protected_families=coverage,
                        generated_states=generated_states,
                        expansions=expansions,
                        frontier_size=len(frontier),
                        reached_targets=tuple(sorted(hit_targets)),
                    )
                )

            if generated_states >= config.max_states:
                terminated_by_state_cap = True
                should_stop = True
                break

            if config.early_stop and len(target_hits) == len(territory.targets):
                should_stop = True
                break

    elapsed_ms = round((perf_counter() - start) * 1000, 3)

    return {
        "strategy": config.strategy,
        "territoryId": territory.id,
        "territoryName": territory.name,
        "combinationId": combination.id,
        "depthLimit": config.depth_limit,
        "budget": territory.budget,
        "targets": list(territory.targets),
        "terminatedByStateCap": terminated_by_state_cap,
        "metrics": {
            "generatedStates": generated_states,
            "expandedStates": expansions,
            "visitedStates": len(visited),
            "executionMs": elapsed_ms,
            "traceLength": len(trace),
            "bestCoverage": best_coverage,
            "targetsReached": len(target_hits),
        },
        "bestState": {
            "positions": [list(position) for position in best_state],
            "protectedFamilies": best_coverage,
        },
        "startState": {
            "positions": [list(position) for position in start_state],
            "protectedFamilies": start_coverage,
        },
        "targetHits": serialize_hits([target_hits[key] for key in sorted(target_hits)]),
        "trace": [serialize_step(step) for step in trace],
    }


def compare_strategies(
    territory: TerritoryProblem,
    combination: StationCombination,
    depth_limit: int,
    max_states: int,
) -> Dict[str, object]:
    bfs = run_search(
        territory,
        combination,
        SearchRunConfig(
            strategy="bfs_limited",
            depth_limit=depth_limit,
            max_trace_steps=1,
            max_states=max_states,
            early_stop=False,
        ),
    )
    dfs = run_search(
        territory,
        combination,
        SearchRunConfig(
            strategy="dfs_limited",
            depth_limit=depth_limit,
            max_trace_steps=1,
            max_states=max_states,
            early_stop=False,
        ),
    )

    return {
        "territoryId": territory.id,
        "combinationId": combination.id,
        "depthLimit": depth_limit,
        "bfs": bfs["metrics"],
        "dfs": dfs["metrics"],
    }
