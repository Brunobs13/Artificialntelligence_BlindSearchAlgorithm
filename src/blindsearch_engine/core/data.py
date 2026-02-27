from __future__ import annotations

from typing import Dict, List

from .models import StationCombination, TerritoryProblem, to_tuple_matrix

RADIUS_COST = {
    1: 4,
    2: 5,
    3: 9,
    4: 17,
}


BUDGET_COMBINATIONS: Dict[int, Dict[int, StationCombination]] = {
    4: {
        1: StationCombination(1, ((1, 1),), (1,)),
    },
    8: {
        1: StationCombination(1, ((1, 1), (1, 5)), (1, 1)),
        2: StationCombination(2, ((2, 4),), (2,)),
    },
    12: {
        1: StationCombination(1, ((2, 2), (6, 6)), (2, 2)),
        2: StationCombination(2, ((1, 1), (1, 7), (7, 1)), (1, 1, 1)),
        3: StationCombination(3, ((4, 3),), (3,)),
    },
    16: {
        1: StationCombination(1, ((1, 1), (1, 9), (9, 1), (9, 9)), (1, 1, 1, 1)),
        2: StationCombination(2, ((3, 3), (8, 8)), (3, 2)),
        3: StationCombination(3, ((2, 2), (2, 8), (8, 8)), (2, 2, 2)),
    },
    20: {
        1: StationCombination(1, ((1, 1), (1, 11), (6, 6), (11, 1), (11, 11)), (1, 1, 1, 1, 1)),
        2: StationCombination(2, ((4, 4),), (4,)),
        3: StationCombination(3, ((3, 3), (9, 9)), (3, 3)),
        4: StationCombination(4, ((2, 2), (2, 10), (10, 2), (10, 10)), (2, 2, 2, 2)),
        5: StationCombination(5, ((3, 3), (10, 2), (2, 10)), (3, 2, 2)),
    },
}


TERRITORIES: Dict[int, TerritoryProblem] = {
    1: TerritoryProblem(
        id=1,
        name="Retail Corridor Alpha",
        matrix=to_tuple_matrix([
            [0, 7, 0, 0, 4],
            [0, 0, 0, 4, 0],
            [1, 0, 0, 0, 0],
            [4, 4, 1, 0, 0],
            [6, 0, 3, 4, 4],
        ]),
        budget=4,
        targets=(19, 20),
        corporate_context="Prioritize high-risk residential clusters around city-center stores.",
    ),
    2: TerritoryProblem(
        id=2,
        name="Retail Corridor Beta",
        matrix=to_tuple_matrix([
            [4, 0, 0, 10, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 6, 3],
            [0, 4, 0, 0, 2],
            [8, 0, 6, 3, 0],
        ]),
        budget=4,
        targets=(21, 22),
        corporate_context="Optimize patrol coverage around high-incident suburban shopping blocks.",
    ),
    3: TerritoryProblem(
        id=3,
        name="Distribution Grid Gamma",
        matrix=to_tuple_matrix([
            [0, 8, 0, 4, 5, 10, 0],
            [0, 4, 0, 7, 0, 4, 0],
            [0, 2, 4, 2, 0, 0, 2],
            [0, 7, 0, 1, 2, 0, 0],
            [2, 4, 0, 0, 3, 0, 2],
            [0, 4, 0, 0, 3, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
        ]),
        budget=8,
        targets=(67, 68),
        corporate_context="Secure logistics feeder routes connected to national distribution centers.",
    ),
    4: TerritoryProblem(
        id=4,
        name="Distribution Grid Delta",
        matrix=to_tuple_matrix([
            [0, 0, 1, 0, 7, 0, 1],
            [0, 1, 4, 0, 0, 0, 4],
            [0, 0, 0, 0, 2, 0, 0],
            [3, 1, 0, 8, 5, 7, 7],
            [0, 4, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 2, 4, 2],
            [0, 8, 3, 6, 3, 0, 0],
        ]),
        budget=8,
        targets=(59, 60),
        corporate_context="Protect mixed-use zones with dynamic employee density and variable threat levels.",
    ),
    5: TerritoryProblem(
        id=5,
        name="Industrial Belt Epsilon",
        matrix=to_tuple_matrix([
            [6, 7, 2, 0, 0, 0, 0, 0, 0],
            [3, 3, 6, 0, 8, 4, 3, 1, 0],
            [0, 0, 8, 0, 0, 0, 2, 4, 0],
            [0, 0, 0, 1, 0, 3, 2, 0, 0],
            [0, 0, 0, 7, 4, 0, 1, 0, 0],
            [12, 8, 0, 5, 4, 1, 4, 3, 4],
            [8, 0, 1, 2, 4, 3, 3, 0, 0],
            [1, 1, 0, 0, 0, 0, 5, 0, 0],
            [4, 0, 0, 0, 4, 6, 0, 13, 2],
        ]),
        budget=12,
        targets=(125, 126),
        corporate_context="Allocate mobile security units across warehouse-heavy neighborhoods.",
    ),
    6: TerritoryProblem(
        id=6,
        name="Industrial Belt Zeta",
        matrix=to_tuple_matrix([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 8, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 1, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 3, 0],
            [0, 0, 2, 4, 0, 0, 0, 1, 0],
            [0, 2, 0, 0, 8, 0, 4, 3, 10],
            [0, 0, 3, 0, 0, 4, 0, 0, 0],
        ]),
        budget=12,
        targets=(57, 58),
        corporate_context="Improve sparse-area emergency response with constrained budget envelopes.",
    ),
    7: TerritoryProblem(
        id=7,
        name="Metro Ring Eta",
        matrix=to_tuple_matrix([
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 11, 2, 0, 0, 9, 3, 0, 0, 3],
            [0, 0, 0, 3, 1, 0, 2, 0, 0, 0, 0],
            [4, 1, 2, 3, 0, 4, 0, 0, 4, 0, 0],
            [5, 0, 0, 0, 4, 0, 1, 0, 4, 3, 0],
            [0, 0, 0, 7, 4, 0, 1, 0, 0, 7, 0],
            [0, 8, 0, 0, 0, 0, 3, 0, 1, 0, 3],
            [0, 3, 0, 0, 5, 2, 3, 0, 0, 0, 2],
            [0, 0, 0, 3, 1, 0, 2, 8, 0, 0, 0],
            [0, 3, 4, 0, 7, 0, 0, 7, 0, 0, 0],
            [4, 2, 0, 4, 0, 3, 0, 0, 5, 7, 0],
        ]),
        budget=16,
        targets=(140, 141),
        corporate_context="Monitor metropolitan perimeter zones with overlapping risk hotspots.",
    ),
    8: TerritoryProblem(
        id=8,
        name="Metro Ring Theta",
        matrix=to_tuple_matrix([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 10, 10, 0, 0, 0, 4, 5, 0, 0],
            [0, 4, 1, 0, 8, 0, 0, 0, 0, 0, 5],
            [8, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 13, 0, 0, 0, 2, 0, 3],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0],
            [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        budget=16,
        targets=(93, 94),
        corporate_context="Balance low-density and high-density patrol corridors in metro outskirts.",
    ),
    9: TerritoryProblem(
        id=9,
        name="National Grid Iota",
        matrix=to_tuple_matrix([
            [2, 4, 0, 0, 6, 7, 3, 4, 0, 0, 3, 0, 1],
            [0, 0, 2, 0, 3, 0, 0, 6, 0, 0, 8, 11, 3],
            [0, 3, 0, 8, 0, 0, 2, 0, 0, 0, 0, 0, 4],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0],
            [0, 6, 0, 8, 0, 3, 0, 0, 0, 0, 0, 0, 1],
            [0, 3, 0, 2, 0, 0, 9, 0, 0, 0, 0, 5, 6],
            [1, 9, 4, 0, 0, 2, 4, 0, 0, 0, 3, 2, 0],
            [2, 3, 0, 4, 0, 0, 0, 6, 2, 0, 1, 0, 3],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 2, 2, 0, 8],
            [7, 2, 4, 2, 0, 0, 6, 4, 1, 0, 0, 0, 7],
            [0, 0, 0, 11, 0, 0, 0, 0, 3, 4, 0, 9, 0],
            [0, 0, 0, 0, 1, 4, 3, 4, 0, 0, 0, 3, 11],
            [0, 0, 4, 7, 7, 0, 0, 2, 0, 2, 5, 0, 1],
        ]),
        budget=20,
        targets=(211, 212),
        corporate_context="Coordinate nationwide strategic response zones for major retail assets.",
    ),
    10: TerritoryProblem(
        id=10,
        name="National Grid Kappa",
        matrix=to_tuple_matrix([
            [0, 0, 1, 4, 0, 0, 9, 0, 0, 0, 12, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 4, 0, 0, 0, 6, 0, 0],
            [0, 6, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 6, 10, 0, 1, 4],
            [0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 1, 3, 0, 0, 0, 0, 9, 0, 0, 0],
            [9, 0, 0, 3, 3, 0, 0, 0, 0, 3, 4, 0, 0],
            [0, 1, 4, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 10],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
        ]),
        budget=20,
        targets=(125, 126),
        corporate_context="Stress-test strategic incident prevention under dense metropolitan complexity.",
    ),
}


def list_territories() -> List[TerritoryProblem]:
    return [TERRITORIES[key] for key in sorted(TERRITORIES)]


def get_territory(territory_id: int) -> TerritoryProblem:
    if territory_id not in TERRITORIES:
        raise KeyError(f"Unknown territory id: {territory_id}")
    return TERRITORIES[territory_id]


def get_combinations_for_budget(budget: int) -> List[StationCombination]:
    combinations = BUDGET_COMBINATIONS.get(budget, {})
    return [combinations[key] for key in sorted(combinations)]


def get_combination(budget: int, combination_id: int) -> StationCombination:
    combinations = BUDGET_COMBINATIONS.get(budget, {})
    if combination_id not in combinations:
        raise KeyError(f"Unknown combination id {combination_id} for budget {budget}")
    return combinations[combination_id]


def get_budget_used(radii: List[int] | tuple[int, ...]) -> int:
    return sum(RADIUS_COST.get(radius, 0) for radius in radii)
