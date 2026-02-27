from blindsearch_engine.core.data import get_combination, get_territory
from blindsearch_engine.core.models import SearchRunConfig
from blindsearch_engine.engine.search import calculate_coverage, compare_strategies, run_search


def test_coverage_calculation_returns_expected_start_value() -> None:
    territory = get_territory(1)
    combination = get_combination(territory.budget, 1)

    coverage, cells = calculate_coverage(combination.stations, combination.radii, territory.matrix)

    assert coverage == 8
    assert len(cells) == 9


def test_bfs_search_reaches_first_target() -> None:
    territory = get_territory(1)
    combination = get_combination(territory.budget, 1)

    result = run_search(
        territory=territory,
        combination=combination,
        config=SearchRunConfig(strategy="bfs_limited", depth_limit=4, max_trace_steps=500, max_states=5000, early_stop=False),
    )

    reached_targets = {hit["target"] for hit in result["targetHits"]}

    assert 19 in reached_targets
    assert result["metrics"]["generatedStates"] >= 1
    assert result["metrics"]["bestCoverage"] >= result["startState"]["protectedFamilies"]


def test_compare_returns_both_strategies() -> None:
    territory = get_territory(2)
    combination = get_combination(territory.budget, 1)

    benchmark = compare_strategies(territory, combination, depth_limit=3, max_states=5000)

    assert "bfs" in benchmark
    assert "dfs" in benchmark
    assert benchmark["bfs"]["generatedStates"] >= 1
    assert benchmark["dfs"]["generatedStates"] >= 1
