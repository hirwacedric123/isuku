document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".feature-card");
  cards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(12px)";
    setTimeout(() => {
      card.style.transition = "opacity 0.35s ease, transform 0.35s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 120 * (index + 1));
  });
});
