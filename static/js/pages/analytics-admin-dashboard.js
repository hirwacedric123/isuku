document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".metric-number");
  counters.forEach((counter) => {
    const target = parseFloat(counter.dataset.count || "0");
    const duration = 700;
    const steps = 25;
    let step = 0;
    const increment = target / steps;
    const timer = setInterval(() => {
      step += 1;
      const value = Math.min(target, increment * step);
      counter.textContent = Number.isInteger(target) ? Math.round(value) : value.toFixed(1);
      if (step >= steps) clearInterval(timer);
    }, duration / steps);
  });

  const chartCanvas = document.getElementById("sector-chart");
  const tableRows = Array.from(document.querySelectorAll("#sector-data-table tbody tr[data-sector]"));
  if (!chartCanvas || tableRows.length === 0 || typeof Chart === "undefined") return;

  const labels = tableRows.map((row) => row.dataset.sector || "");
  const totals = tableRows.map((row) => Number(row.dataset.total || "0"));
  const theme = window.isukuChartTheme;
  const baseOptions = theme?.getBaseOptions ? theme.getBaseOptions() : {};

  new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Reports",
          data: totals,
          borderRadius: 10,
          backgroundColor: ["#043915", "#4C763B", "#B0CE88", "#FFFD8F", "#3B5E2E", "#6A904B"],
          borderColor: "#043915",
          borderWidth: 1,
        },
      ],
    },
    options: {
      ...baseOptions,
      plugins: {
        ...baseOptions.plugins,
        tooltip: {
          backgroundColor: "#043915",
          titleColor: "#FFFD8F",
          bodyColor: "#fff",
          padding: 10,
        },
      },
    },
  });
});
