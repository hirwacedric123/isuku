window.isukuChartTheme = {
  colors: {
    primary: "#043915",
    secondary: "#4C763B",
    soft: "#B0CE88",
    accent: "#FFFD8F",
    text: "#102018",
    grid: "rgba(76, 118, 59, 0.2)",
  },
  getBaseOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: this.colors.text,
            font: { size: 12, weight: 600 },
          },
        },
      },
      scales: {
        x: {
          ticks: { color: this.colors.text },
          grid: { color: this.colors.grid },
        },
        y: {
          beginAtZero: true,
          ticks: { color: this.colors.text, precision: 0 },
          grid: { color: this.colors.grid },
        },
      },
    };
  },
};
