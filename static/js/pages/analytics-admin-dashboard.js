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
});
