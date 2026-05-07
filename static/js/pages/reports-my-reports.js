document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("reports-search");
  const rows = Array.from(document.querySelectorAll(".report-table tbody tr"));
  if (!search || rows.length === 0) return;

  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();
    rows.forEach((row) => {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(query) ? "" : "none";
    });
  });
});
