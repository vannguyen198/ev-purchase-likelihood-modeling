type ViewName = "overview" | "metrics" | "differences" | "why";
type MetricGroup = "all" | "ranking" | "calibration" | "distribution";

interface EffectivenessRow {
  group: MetricGroup;
  area: string;
  logistic: string;
  catboost: string;
  winner: string;
  reason: string;
}

interface DifferenceRow {
  id: number;
  logistic: number;
  catboost: number;
  difference: number;
  traits: string;
}

const effectivenessRows: EffectivenessRow[] = [
  {
    group: "ranking",
    area: "Ranking likely buyers",
    logistic: "ROC AUC 0.937953",
    catboost: "ROC AUC 0.940719",
    winner: "CatBoost",
    reason: "Higher AUC means better ordering of likely buyers above unlikely buyers.",
  },
  {
    group: "calibration",
    area: "Probability quality",
    logistic: "Log loss 0.233580",
    catboost: "Log loss 0.320222",
    winner: "Logistic",
    reason: "Lower log loss means the probabilities were better calibrated in validation.",
  },
  {
    group: "distribution",
    area: "Prediction spread",
    logistic: "Mean 0.174844, median 0.024020",
    catboost: "Mean 0.294772, median 0.087422",
    winner: "Depends",
    reason: "CatBoost is more confident; useful for ranking, risky for log-loss scoring.",
  },
  {
    group: "ranking",
    area: "Feature interactions",
    logistic: "Limited without manual feature engineering",
    catboost: "Learns interactions naturally",
    winner: "CatBoost",
    reason: "Tree boosting can combine subsidy, charging access, anxiety, commute, and city type.",
  },
  {
    group: "calibration",
    area: "Explainability",
    logistic: "Clear linear feature weights",
    catboost: "More complex tree ensemble",
    winner: "Logistic",
    reason: "Logistic regression is easier to audit and explain as additive contributions.",
  },
  {
    group: "distribution",
    area: "Rows above 0.5",
    logistic: "45,773 rows",
    catboost: "84,415 rows",
    winner: "Depends",
    reason: "CatBoost identifies many more high-likelihood IDs; whether that helps depends on the metric.",
  },
];

const differenceRows: DifferenceRow[] = [
  {
    id: 702729,
    logistic: 0.11801,
    catboost: 0.74526,
    difference: 0.62725,
    traits: "Subsidy yes, home charging yes, low range anxiety, short commute",
  },
  {
    id: 695839,
    logistic: 0.119238,
    catboost: 0.710772,
    difference: 0.591534,
    traits: "Rural, subsidy yes, home charging yes, low range anxiety",
  },
  {
    id: 859836,
    logistic: 0.260082,
    catboost: 0.845603,
    difference: 0.585522,
    traits: "Higher income, suburban, subsidy yes, short commute",
  },
  {
    id: 699784,
    logistic: 0.56351,
    catboost: 0.244665,
    difference: -0.318845,
    traits: "High concern, long commute, rural, subsidy yes",
  },
  {
    id: 947946,
    logistic: 0.561905,
    catboost: 0.270939,
    difference: -0.290966,
    traits: "High concern, long commute, rural, home charging yes",
  },
];

const metricTable = document.querySelector<HTMLDivElement>("#metric-table");
const differenceTable = document.querySelector<HTMLDivElement>("#difference-table");
const metricSelect = document.querySelector<HTMLSelectElement>("#metric-select");
const tabs = Array.from(document.querySelectorAll<HTMLButtonElement>(".tab"));
const panels = Array.from(document.querySelectorAll<HTMLElement>(".view"));

function formatProbability(value: number): string {
  return value.toFixed(6);
}

function winnerClass(winner: string): string {
  return winner === "Depends" ? "winner mixed" : "winner";
}

function renderMetricTable(group: MetricGroup = "all"): void {
  if (!metricTable) {
    return;
  }

  const rows = effectivenessRows.filter((row) => group === "all" || row.group === group);
  metricTable.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Comparison Area</th>
          <th>Logistic Regression</th>
          <th>CatBoost</th>
          <th>More Effective</th>
          <th>Why</th>
        </tr>
      </thead>
      <tbody>
        ${rows
          .map(
            (row) => `
              <tr>
                <td>${row.area}</td>
                <td>${row.logistic}</td>
                <td>${row.catboost}</td>
                <td><span class="${winnerClass(row.winner)}">${row.winner}</span></td>
                <td>${row.reason}</td>
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function renderDifferenceTable(): void {
  if (!differenceTable) {
    return;
  }

  differenceTable.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Logistic</th>
          <th>CatBoost</th>
          <th>CatBoost - Logistic</th>
          <th>Row Pattern</th>
        </tr>
      </thead>
      <tbody>
        ${differenceRows
          .map(
            (row) => `
              <tr>
                <td class="number">${row.id}</td>
                <td class="number">${formatProbability(row.logistic)}</td>
                <td class="number">${formatProbability(row.catboost)}</td>
                <td class="number">${formatProbability(row.difference)}</td>
                <td>${row.traits}</td>
              </tr>
            `,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function activateView(viewName: ViewName): void {
  tabs.forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.view === viewName);
  });

  panels.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.panel === viewName);
  });
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    activateView(tab.dataset.view as ViewName);
  });
});

metricSelect?.addEventListener("change", () => {
  renderMetricTable(metricSelect.value as MetricGroup);
});

renderMetricTable();
renderDifferenceTable();
