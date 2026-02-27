const state = {
  territories: [],
  territory: null,
  combinations: [],
  combination: null,
  runResult: null,
  trace: [],
  stepIndex: 0,
  timer: null,
  speedMs: 350,
};

const els = {
  health: document.getElementById("health-pill"),
  territorySelect: document.getElementById("territory-select"),
  combinationSelect: document.getElementById("combination-select"),
  strategySelect: document.getElementById("strategy-select"),
  depthLimit: document.getElementById("depth-limit"),
  maxStates: document.getElementById("max-states"),
  runBtn: document.getElementById("run-btn"),
  compareBtn: document.getElementById("compare-btn"),
  context: document.getElementById("corporate-context"),
  message: document.getElementById("message"),
  mapMeta: document.getElementById("map-meta"),
  grid: document.getElementById("grid"),
  playBtn: document.getElementById("play-btn"),
  pauseBtn: document.getElementById("pause-btn"),
  stepPrevBtn: document.getElementById("step-prev-btn"),
  stepNextBtn: document.getElementById("step-next-btn"),
  speedRange: document.getElementById("speed-range"),
  stepLabel: document.getElementById("step-label"),
  metrics: document.getElementById("metrics"),
  targets: document.getElementById("targets"),
  comparison: document.getElementById("comparison"),
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || payload.error || `Request failed (${response.status})`);
  }
  return payload;
}

function setMessage(text, isError = false) {
  els.message.textContent = text;
  els.message.classList.toggle("error", isError);
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString("en-US");
}

function stopPlayback() {
  if (state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
}

function calculateCoveredCells(positions, radii, rows, cols) {
  const covered = new Set();
  positions.forEach((station, idx) => {
    const [cx, cy] = station;
    const radius = radii[idx];
    for (let x = cx - radius; x <= cx + radius; x += 1) {
      for (let y = cy - radius; y <= cy + radius; y += 1) {
        if (x >= 0 && x < rows && y >= 0 && y < cols) {
          covered.add(`${x}:${y}`);
        }
      }
    }
  });
  return covered;
}

function renderGrid(step = null) {
  if (!state.territory) {
    els.grid.innerHTML = "";
    return;
  }

  const matrix = state.territory.matrix;
  const rows = matrix.length;
  const cols = matrix[0].length;
  els.grid.style.gridTemplateColumns = `repeat(${cols}, minmax(28px, 1fr))`;

  const positions = step?.positions || state.combination?.stations || [];
  const radii = state.combination?.radii || [];
  const coveredCells = calculateCoveredCells(positions, radii, rows, cols);
  const stationCells = new Set(positions.map(([x, y]) => `${x}:${y}`));

  const cells = [];
  for (let x = 0; x < rows; x += 1) {
    for (let y = 0; y < cols; y += 1) {
      const value = matrix[x][y];
      const key = `${x}:${y}`;
      const classes = ["cell"];
      if (value >= 7) classes.push("hot");
      if (coveredCells.has(key)) classes.push("covered");
      if (stationCells.has(key)) classes.push("station");
      cells.push(`<div class="${classes.join(" ")}" title="(${x},${y}) risk=${value}">${value}</div>`);
    }
  }

  els.grid.innerHTML = cells.join("");
}

function renderMetrics() {
  const metrics = state.runResult?.metrics;
  if (!metrics) {
    els.metrics.innerHTML = "";
    return;
  }

  const cards = [
    ["Generated States", formatNumber(metrics.generatedStates)],
    ["Expanded States", formatNumber(metrics.expandedStates)],
    ["Execution (ms)", formatNumber(metrics.executionMs)],
    ["Best Coverage", formatNumber(metrics.bestCoverage)],
    ["Targets Reached", `${metrics.targetsReached}/${state.runResult.targets.length}`],
    ["Trace Length", formatNumber(metrics.traceLength)],
  ];

  els.metrics.innerHTML = cards
    .map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
}

function renderTargets() {
  const hits = state.runResult?.targetHits || [];
  if (!hits.length) {
    els.targets.innerHTML = "<li>No targets reached with current limits.</li>";
    return;
  }

  els.targets.innerHTML = hits
    .map(
      (hit) =>
        `<li>Target ${hit.target} reached at step ${hit.stepIndex} (depth ${hit.depth}) with coverage ${hit.coverage}.</li>`
    )
    .join("");
}

function renderStep(index) {
  if (!state.trace.length) {
    els.stepLabel.textContent = "Step: -";
    renderGrid();
    return;
  }

  state.stepIndex = Math.max(0, Math.min(index, state.trace.length - 1));
  const step = state.trace[state.stepIndex];
  els.stepLabel.textContent = `Step ${step.index} · depth ${step.depth} · protected ${step.protectedFamilies} · frontier ${step.frontierSize}`;
  renderGrid(step);
}

function playTrace() {
  if (!state.trace.length) {
    setMessage("Run a simulation first.", true);
    return;
  }

  stopPlayback();
  state.timer = setInterval(() => {
    if (state.stepIndex >= state.trace.length - 1) {
      stopPlayback();
      return;
    }
    renderStep(state.stepIndex + 1);
  }, state.speedMs);
}

function renderComparison(payload) {
  const maxGenerated = Math.max(payload.bfs.generatedStates, payload.dfs.generatedStates, 1);
  const bfsPct = Math.round((payload.bfs.generatedStates / maxGenerated) * 100);
  const dfsPct = Math.round((payload.dfs.generatedStates / maxGenerated) * 100);

  els.comparison.innerHTML = `
    <div><strong>BFS Limited</strong> · ${formatNumber(payload.bfs.generatedStates)} states · ${formatNumber(payload.bfs.executionMs)} ms</div>
    <div class="bar bfs"><i style="width:${bfsPct}%"></i></div>
    <div style="margin-top:8px"><strong>DFS Limited</strong> · ${formatNumber(payload.dfs.generatedStates)} states · ${formatNumber(payload.dfs.executionMs)} ms</div>
    <div class="bar dfs"><i style="width:${dfsPct}%"></i></div>
  `;
}

async function loadHealth() {
  try {
    const payload = await api("/health");
    els.health.textContent = `${payload.service} · ${payload.status}`;
  } catch (error) {
    els.health.textContent = "Service unavailable";
    setMessage(error.message, true);
  }
}

function refreshCombinationSelect() {
  els.combinationSelect.innerHTML = state.combinations
    .map((c) => `<option value="${c.id}">#${c.id} · radii [${c.radii.join(",")}] · budget ${c.budgetUsed}</option>`)
    .join("");

  state.combination = state.combinations[0] || null;
}

async function loadTerritory(territoryId) {
  const payload = await api(`/api/territories/${territoryId}`);
  state.territory = payload;
  state.combinations = payload.combinations || [];
  refreshCombinationSelect();

  els.context.textContent = payload.corporateContext;
  els.mapMeta.textContent = `${payload.name} · ${payload.matrix.length}x${payload.matrix[0].length} · budget ${payload.budget} · targets ${payload.targets.join(", ")}`;

  state.runResult = null;
  state.trace = [];
  renderMetrics();
  renderTargets();
  renderStep(0);
}

async function loadInitialData() {
  const payload = await api("/api/territories");
  state.territories = payload.territories;

  els.territorySelect.innerHTML = state.territories
    .map((t) => `<option value="${t.id}">#${t.id} ${t.name}</option>`)
    .join("");

  if (!state.territories.length) {
    throw new Error("No territories available.");
  }

  await loadTerritory(state.territories[0].id);
}

async function runSimulation() {
  if (!state.territory) {
    setMessage("Load a territory first.", true);
    return;
  }

  stopPlayback();
  setMessage("Running simulation...");

  const payload = {
    territory_id: Number(els.territorySelect.value),
    combination_id: Number(els.combinationSelect.value),
    strategy: els.strategySelect.value,
    depth_limit: Number(els.depthLimit.value),
    max_states: Number(els.maxStates.value),
    max_trace_steps: 2500,
    early_stop: false,
  };

  try {
    const result = await api("/api/run", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    state.combination = state.combinations.find((item) => item.id === payload.combination_id) || state.combination;
    state.runResult = result;
    state.trace = result.trace || [];

    renderMetrics();
    renderTargets();
    renderStep(0);

    const termination = result.terminatedByStateCap ? " (state cap reached)" : "";
    setMessage(`Simulation complete: ${result.metrics.generatedStates} states generated${termination}.`);
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function compareStrategies() {
  if (!state.territory) {
    setMessage("Load a territory first.", true);
    return;
  }

  setMessage("Running benchmark...");
  const payload = {
    territory_id: Number(els.territorySelect.value),
    combination_id: Number(els.combinationSelect.value),
    depth_limit: Number(els.depthLimit.value),
    max_states: Number(els.maxStates.value),
  };

  try {
    const result = await api("/api/compare", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    renderComparison(result);
    setMessage("Benchmark complete.");
  } catch (error) {
    setMessage(error.message, true);
  }
}

function wireEvents() {
  els.territorySelect.addEventListener("change", async () => {
    try {
      await loadTerritory(Number(els.territorySelect.value));
      setMessage("Territory loaded.");
    } catch (error) {
      setMessage(error.message, true);
    }
  });

  els.combinationSelect.addEventListener("change", () => {
    state.combination = state.combinations.find((item) => item.id === Number(els.combinationSelect.value)) || null;
    renderGrid();
  });

  els.runBtn.addEventListener("click", runSimulation);
  els.compareBtn.addEventListener("click", compareStrategies);

  els.playBtn.addEventListener("click", playTrace);
  els.pauseBtn.addEventListener("click", stopPlayback);
  els.stepPrevBtn.addEventListener("click", () => {
    stopPlayback();
    renderStep(state.stepIndex - 1);
  });
  els.stepNextBtn.addEventListener("click", () => {
    stopPlayback();
    renderStep(state.stepIndex + 1);
  });

  els.speedRange.addEventListener("input", (event) => {
    state.speedMs = Number(event.target.value);
    if (state.timer) {
      playTrace();
    }
  });
}

async function bootstrap() {
  wireEvents();

  try {
    await Promise.all([loadHealth(), loadInitialData()]);
    setMessage("Control room initialized.");
  } catch (error) {
    setMessage(error.message, true);
  }
}

bootstrap();
